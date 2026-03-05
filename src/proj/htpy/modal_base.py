import htpy as h

from proj.text import tm

from .util import HtpyComponent


class ModalBase(HtpyComponent):
    def title(self):
        return None

    def body(self):
        return None

    def close_button_text(self):
        return tm("close")

    def render(self):
        return h.div(id="modal-mount-point", hx_swap_oob="outerHTML")[
            h.div(
                ".modal.modal-xl.fade",
                tabindex="-1",
                id="modal",
                aria_hidden="true",
            )[
                h.div(".modal-dialog")[
                    h.div(".modal-content")[
                        h.div(".modal-header")[self.title()],
                        h.div(".modal-body.overflow-auto")[self.body()],
                        h.div(".modal-footer")[
                            h.button(
                                type="button",
                                class_="btn btn-secondary",
                                data_bs_dismiss="modal",
                            )[self.close_button_text()],
                        ],
                    ],
                ],
            ],
        ]


class ModalBaseTemplate(ModalBase):
    def __init__(self, context, request):
        super().__init__()
        self.context = context
        self.request = request
