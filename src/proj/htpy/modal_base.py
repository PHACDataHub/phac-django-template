from django.http import HttpResponse
from django.views import View

import htpy as h

from proj.text import tm

from .util import HtpyComponent


@h.with_children
def ModalComponent(
    children,
    *,
    title=None,
    size_cls=None,
    modal_id=None,
    close_button_text=None,
):

    if not close_button_text:
        close_button_text = tm("close")

    wrapper_attrs = {
        "data_modal": True,
        "aria_hidden": "true",
    }
    if modal_id:
        wrapper_attrs["id"] = modal_id

    return h.div(**wrapper_attrs)[
        h.div(class_=["modal-dialog", size_cls])[
            h.div(".modal-content.p-2")[
                h.div(".modal-header")[
                    h.div[title],
                    h.button(
                        type="button",
                        class_="btn-close",
                        data_modal_close=True,
                        aria_label="Close",
                    ),
                ],
                h.div(".modal-body", id="modal-body")[children],
                h.div(".modal-footer")[
                    h.button(
                        type="button",
                        class_="btn btn-secondary",
                        data_modal_close=True,
                    )[close_button_text],
                ],
            ],
        ],
    ]
