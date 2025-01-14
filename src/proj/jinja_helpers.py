from urllib.parse import quote, urlencode, urlparse, urlunparse

from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import activate, get_language, override

import phac_aspc.django.helpers.templatetags as phac_aspc
from django_htmx.templatetags.django_htmx import django_htmx_script
from jinja2 import Environment, pass_context
from jinja2.ext import Extension, nodes
from phac_aspc.rules import test_rule

from .text import tdt, tm

_to_add_to_env = {}


def add_to_env(func, name=None):
    if name is None:
        name = func.__name__
    _to_add_to_env[name] = func

    return func


@add_to_env
@pass_context
def respects_rule(context, rule, obj=None):
    user = context["request"].user
    if not user.is_authenticated:
        return False
    return test_rule(rule, user, obj)


class LanguageExtension(Extension):
    tags = {"language"}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        # Parse the language code argument
        args = [parser.parse_expression()]
        # Parse everything between the start and end tag:
        body = parser.parse_statements(["name:endlanguage"], drop_needle=True)
        # Call the _switch_language method with the given language code and body
        return nodes.CallBlock(
            self.call_method("_switch_language", args), [], [], body
        ).set_lineno(lineno)

    def _switch_language(self, language_code, caller):
        with override(language_code):
            # Temporarily override the active language and render the body
            output = caller()
        return output


def convert_url_other_lang(url_str):
    parsed_url = urlparse(url_str)
    path = parsed_url.path
    query = parsed_url.query

    if "fr-ca" in path:
        new_path = path.replace("/fr-ca", "")
    else:
        new_path = "/fr-ca" + path

    new_url = parsed_url._replace(path=new_path)

    if "login" in path and "next" in query:
        if "fr-ca" in path:
            new_query = query.replace("next=/fr-ca", "next=")
        else:
            new_query = query.replace("next=", "next=/fr-ca")
    else:
        new_query = query

    new_url = new_url._replace(query=new_query)

    return urlunparse(new_url)


@add_to_env
@pass_context
def url_to_other_lang(context):
    """
    Provides the URL to the other language:
    For example, if current language is English then it will provide
    the url to the French language.
    """
    request = context["request"]
    full_uri = request.get_full_path()
    return convert_url_other_lang(full_uri)


@add_to_env
def get_lang_code():
    """
    Provides the language code for the current language
    """
    current_lang = get_language()
    return current_lang.lower()


def get_other_lang_code():
    """
    Provides the language code for the other language (Ex. if current lang
    is en-ca, then the other lang is fr-ca), this is currently used for
    setting the lang tag in the button switch UI
    """
    current_lang = get_language()
    if "en" in current_lang.lower():
        return "fr-ca"
    return "en-ca"


@add_to_env
def get_other_lang():
    """
    Returns the language not currently being used (Ex. if current lang
    is en, then the other lang is French.  This is used as the label for the
    button to switch languages)
    """
    current_lang = get_language()
    if "en" in current_lang.lower():
        return "Français"
    return "English"


@add_to_env
def message_type(message):
    # remaps the message level tag to the bootstrap alert type
    if message.level_tag == "error":
        return "danger"
    else:
        return f"{message.level_tag}"


@add_to_env
@pass_context
def ipython(context):
    from IPython import embed

    embed()
    return ""


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            **_to_add_to_env,
            "getattr": getattr,
            "hasattr": hasattr,
            "len": len,
            "list": list,
            "url": reverse,
            "urlencode": urlencode,
            "static": static,
            "phac_aspc": phac_aspc,
            "tm": tm,
            "tdt": tdt,
            "print": print,
            "django_htmx_script": django_htmx_script,
        }
    )
    env.filters["quote"] = lambda x: quote(str(x))
    return env
