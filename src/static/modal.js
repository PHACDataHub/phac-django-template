// NOTE : This is mostly AI-written, probably over-engineered and buggy
// why not stick with bootstrap or another lib? 
// nested modals, HTMX integration and focus management are a pain to wedge in
// once this is stable and used in a few places, move to helpers repo

// ── Modal Stack Manager ──
// also depends on modal.css and bootstrap css
//
// A custom modal system supporting stacked/nested modals, HTMX integration,
// focus trapping, and accessible keyboard handling. Uses Bootstrap CSS for
// styling but does NOT use Bootstrap's JS modal — all behavior is managed here
//
// ## Data attributes
//
//   [data-modal]            Marks an element as a modal container.
//   [data-modal-slot]       Landing zone for HTMX-swapped modals (one in base template)
//   [data-modal-open="id"]  Click opens the static modal with that DOM id.
//   [data-modal-close]      Click closes the nearest ancestor [data-modal].
//
// ## Opening modals
//
//   Static (already in DOM):
//     <button data-modal-open="my-modal">Open</button>
//     <div id="my-modal" data-modal aria-hidden="true">…</div>
//
//   Via HTMX (fetched from server):
//     <button hx-get="/my-modal/" hx-target="#modal-slot" hx-swap="innerHTML">
//     The view returns a ModalBase fragment. On htmx:afterSettle, any new
//     [data-modal] inside [data-modal-slot] is auto-opened.
//
//   Nested: open a modal from inside another modal. Each gets its own
//     backdrop and z-index. Escape closes only the topmost one.
//
// ## Forms in modals (ModalFormView pattern)
//
//   ModalFormView handles GET (render modal) and POST (validate) on one route.
//   The form uses hx_post targeting #modal-body (inside the open modal), so:
//     - On validation error: only the body is swapped, modal stays open.
//     - On success: the view returns 204 + HX-Trigger: modal-close.
//
//   Potential issues:
//     - The form's hx_post must target #modal-body, NOT the whole modal.
//       Targeting the modal itself would cause the JS to see a new [data-modal]
//       in the slot and try to re-open it.
//     - If your success response includes HTML (not 204), make sure it does
//       NOT contain [data-modal] elements or they'll auto-open.
//     - CSRF: the base template's htmx:configRequest listener adds the token
//       automatically, so forms don't need a hidden csrf input for HTMX posts.
//       But they DO need it for non-HTMX fallback submissions.
//
// ## Accessibility
//
//   - Focus is trapped inside the topmost modal (Tab/Shift+Tab cycle).
//   - On close, focus returns to the element that was focused before opening.
//     For nested modals, focus goes back into the parent modal.
//   - After an HTMX swap inside a modal (e.g. form errors), focus moves to
//     the first .alert-danger element, or the first focusable element.
//   - Modals have role="dialog" and aria-modal="true" while open.
//   - Backdrop clicks and Escape key close the topmost modal
//

const ModalStack = (() => {
    const stack = []; // array of { el, previousFocus, backdrop }
    const BASE_Z = 1050;
    const Z_STEP = 20;

    function currentZ() {
        return BASE_Z + stack.length * Z_STEP;
    }

    function createBackdrop(modal) {
        const bd = document.createElement("div");
        bd.className = "modal-stack-backdrop";
        bd.style.cssText = `
      position:fixed;inset:0;
      background:rgba(0,0,0,0.5);
      z-index:${currentZ() - 1};
    `;
        bd.setAttribute("aria-hidden", "true");
        // Insert as a sibling right before the modal so both share the
        // same stacking context. Appending to <body> would cause z-index
        // conflicts when modals are nested inside other modals.
        modal.parentElement.insertBefore(bd, modal);
        return bd;
    }

    const FOCUSABLE =
        'a[href],button:not([disabled]),textarea:not([disabled]),' +
        'input:not([disabled]),select:not([disabled]),[tabindex]:not([tabindex="-1"])';

    function setupFocusTrap(el) {
        function handler(e) {
            if (e.key !== "Tab") return;
            const nodes = Array.from(el.querySelectorAll(FOCUSABLE)).filter(
                (n) => n.offsetParent !== null
            );
            if (!nodes.length) return;
            const first = nodes[0];
            const last = nodes[nodes.length - 1];
            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault();
                last.focus();
            } else if (!e.shiftKey && document.activeElement === last) {
                e.preventDefault();
                first.focus();
            }
        }
        el._modalTrapHandler = handler;
        el.addEventListener("keydown", handler);
    }

    function removeFocusTrap(el) {
        if (el._modalTrapHandler) {
            el.removeEventListener("keydown", el._modalTrapHandler);
            delete el._modalTrapHandler;
        }
    }

    function focusFirst(el) {
        const target = el.querySelector(FOCUSABLE);
        if (target) {
            target.focus();
        } else {
            el.setAttribute("tabindex", "-1");
            el.focus();
        }
    }

    function open(el) {
        if (stack.some((entry) => entry.el === el)) return;

        const previousFocus = document.activeElement;
        const backdrop = createBackdrop(el);

        el.style.zIndex = currentZ();
        el.setAttribute("role", "dialog");
        el.setAttribute("aria-modal", "true");
        el.classList.add("modal-open");
        el.removeAttribute("aria-hidden");

        stack.push({ el, previousFocus, backdrop });
        document.body.classList.add("modal-stack-active");

        setupFocusTrap(el);

        requestAnimationFrame(() => {
            el.classList.add("modal-visible");
            focusFirst(el);
        });
    }

    function close(el) {
        const idx = stack.findIndex((entry) => entry.el === el);
        if (idx === -1) return;

        const entry = stack[idx];
        stack.splice(idx, 1);

        el.classList.remove("modal-visible");
        removeFocusTrap(el);

        let cleaned = false;
        const onEnd = () => {
            if (cleaned) return;
            cleaned = true;

            el.classList.remove("modal-open");
            el.setAttribute("aria-hidden", "true");
            el.style.zIndex = "";

            if (entry.backdrop && entry.backdrop.parentNode) {
                entry.backdrop.parentNode.removeChild(entry.backdrop);
            }

            // Only clear the slot if this modal is a direct child of it.
            // Nested modals inside another modal's body must not clear the slot,
            // or they'd destroy the parent modal while leaving its backdrop.
            const parent = el.parentElement;
            if (parent && parent.hasAttribute("data-modal-slot")) {
                parent.innerHTML = "";
            }

            if (!stack.length) {
                document.body.classList.remove("modal-stack-active");
            }

            // Restore focus into the parent modal if one is still open,
            // otherwise back to the element that originally triggered the modal.
            if (stack.length) {
                const topModal = stack[stack.length - 1].el;
                if (entry.previousFocus && topModal.contains(entry.previousFocus)) {
                    entry.previousFocus.focus();
                } else {
                    focusFirst(topModal);
                }
            } else if (entry.previousFocus && entry.previousFocus.focus) {
                entry.previousFocus.focus();
            }

            el.dispatchEvent(new CustomEvent("modal-closed", { bubbles: true }));
        };

        el.addEventListener("transitionend", (e) => {
            if (e.target === el) onEnd();
        }, { once: true });
        setTimeout(onEnd, 300);
    }

    function closeCurrent() {
        if (stack.length) {
            close(stack[stack.length - 1].el);
        }
    }

    function isOpen(el) {
        return stack.some((entry) => entry.el === el);
    }

    return { open, close, closeCurrent, isOpen, focusFirst, stack };
})();


// ── Event listeners ──

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        ModalStack.closeCurrent();
    }
});

document.addEventListener("click", (e) => {
    if (e.target.classList.contains("modal-stack-backdrop")) {
        ModalStack.closeCurrent();
    }
});

document.addEventListener("click", (e) => {
    const closeBtn = e.target.closest("[data-modal-close]");
    if (!closeBtn) return;
    const modal = closeBtn.closest("[data-modal]");
    if (modal) ModalStack.close(modal);
});

document.addEventListener("click", (e) => {
    const openBtn = e.target.closest("[data-modal-open]");
    if (!openBtn) return;
    e.preventDefault();
    const modal = document.getElementById(openBtn.getAttribute("data-modal-open"));
    if (modal) ModalStack.open(modal);
});

// After HTMX swaps inside a modal (e.g. form re-render with errors),
// move focus to the first error or first focusable element.
document.body.addEventListener("htmx:afterSettle", (e) => {
    if (!ModalStack.stack.length) return;
    const topModal = ModalStack.stack[ModalStack.stack.length - 1].el;
    if (!topModal.contains(e.target)) return;
    if (e.target.hasAttribute("data-modal-slot")) return;

    const error = topModal.querySelector(".alert-danger");
    if (error) {
        error.setAttribute("tabindex", "-1");
        error.focus();
        return;
    }
    ModalStack.focusFirst(topModal);
});

// Auto-open any [data-modal] swapped into a [data-modal-slot].
document.body.addEventListener("htmx:afterSettle", (e) => {
    document.querySelectorAll("[data-modal-slot] [data-modal]").forEach((modal) => {
        if (!ModalStack.isOpen(modal)) {
            ModalStack.open(modal);
        }
    });
});

// Close the topmost modal via HX-Trigger response header.
// Usage: resp["HX-Trigger"] = "modal-close"
// Note: if you notice issues, try HX-Trigger-After-Settle instead
document.addEventListener("modal-close", () => {
    ModalStack.closeCurrent();
});
