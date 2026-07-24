"""Contract tests for explicit paid-provider activation."""

from __future__ import annotations

from unittest import mock

from lib import env, permission_preflight, pipeline


def _load(monkeypatch, tmp_path, values: dict[str, str]):
    for key in {
        *[item for keys in env.PAID_PROVIDER_KEYS.values() for item in keys],
        env.PAID_PROVIDERS_ENV,
        "SCRAPE_CREATORS_API_KEY",
    }:
        monkeypatch.delenv(key, raising=False)
    for key, value in values.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setattr(env, "CONFIG_FILE", None)
    monkeypatch.chdir(tmp_path)
    with mock.patch.object(env, "_load_keychain", return_value={}), \
         mock.patch.object(env, "_load_pass", return_value={}):
        return env.get_config(policy=env.ConfigLoadPolicy(browser_cookies="plan_only"))


def test_configured_paid_key_is_inert_without_allowlist(monkeypatch, tmp_path):
    config = _load(monkeypatch, tmp_path, {"XAI_API_KEY": "xai_dummy_value"})

    assert config["XAI_API_KEY"] is None
    assert config["_PAID_PROVIDER_ALLOWLIST"] == []
    assert config["_BLOCKED_PAID_PROVIDERS"] == ["xai"]


def test_allowlisted_paid_key_remains_available(monkeypatch, tmp_path):
    config = _load(
        monkeypatch,
        tmp_path,
        {
            "XAI_API_KEY": "xai_dummy_value",
            env.PAID_PROVIDERS_ENV: "xai",
        },
    )

    assert config["XAI_API_KEY"] == "xai_dummy_value"
    assert config["_PAID_PROVIDER_ALLOWLIST"] == ["xai"]
    assert config["_BLOCKED_PAID_PROVIDERS"] == []


def test_aliases_are_canonicalized_and_unknown_names_are_reported(monkeypatch, tmp_path):
    config = _load(
        monkeypatch,
        tmp_path,
        {
            "GEMINI_API_KEY": "gemini_dummy_value",
            env.PAID_PROVIDERS_ENV: "gemini,typo-provider",
        },
    )

    assert config["GEMINI_API_KEY"] == "gemini_dummy_value"
    assert config["_PAID_PROVIDER_ALLOWLIST"] == ["google"]
    assert config["_UNKNOWN_PAID_PROVIDERS"] == ["typo-provider"]


def test_hosted_provider_requires_explicit_allowlist(monkeypatch, tmp_path):
    blocked = _load(
        monkeypatch,
        tmp_path,
        {"LAST30DAYS_API_KEY": "hosted_dummy_value"},
    )
    assert "hosted" in blocked["_BLOCKED_PAID_PROVIDERS"]
    assert env.paid_provider_allowed(blocked, "hosted") is False

    allowed = _load(
        monkeypatch,
        tmp_path,
        {
            "LAST30DAYS_API_KEY": "hosted_dummy_value",
            env.PAID_PROVIDERS_ENV: "hosted",
        },
    )
    assert env.paid_provider_allowed(allowed, "hosted") is True


def test_preflight_reports_provider_names_without_secret_values(monkeypatch, tmp_path):
    secret = "xai_dummy_never_render"
    config = _load(monkeypatch, tmp_path, {"XAI_API_KEY": secret})
    diagnose = pipeline.diagnose(config, safe=True)
    preflight = permission_preflight.build(config, diagnose)
    rendered = permission_preflight.render_text(preflight)

    assert preflight["network"]["paid_providers"]["blocked"] == ["xai"]
    assert "xai" in rendered
    assert secret not in str(preflight)
    assert secret not in rendered


def test_keychain_and_pass_do_not_probe_blocked_paid_credentials(monkeypatch, tmp_path):
    seen: dict[str, list[str]] = {}
    monkeypatch.setattr(env, "CONFIG_FILE", None)
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv(env.PAID_PROVIDERS_ENV, raising=False)

    def fake_keychain(keys, aliases=None):
        seen["keychain"] = list(keys)
        return {}

    def fake_pass(keys, prefix):
        seen["pass"] = list(keys)
        return {}

    with mock.patch.object(env, "_load_keychain", side_effect=fake_keychain), \
         mock.patch.object(env, "_load_pass", side_effect=fake_pass):
        env.get_config()

    assert "XAI_API_KEY" not in seen["keychain"]
    assert "OPENAI_API_KEY" not in seen["keychain"]
    assert "XAI_API_KEY" not in seen["pass"]
    assert "AUTH_TOKEN" in seen["keychain"]


def test_explicit_empty_process_allowlist_overrides_file(monkeypatch, tmp_path):
    config_file = tmp_path / ".env"
    config_file.write_text(
        "XAI_API_KEY=xai_dummy_value\n"
        "LAST30DAYS_PAID_PROVIDERS=xai\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(env, "CONFIG_FILE", config_file)
    monkeypatch.setenv(env.PAID_PROVIDERS_ENV, "")
    monkeypatch.chdir(tmp_path)

    with mock.patch.object(env, "_load_keychain", return_value={}), \
         mock.patch.object(env, "_load_pass", return_value={}):
        config = env.get_config()

    assert config["XAI_API_KEY"] is None
    assert config["_PAID_PROVIDER_ALLOWLIST"] == []
    assert config["_BLOCKED_PAID_PROVIDERS"] == ["xai"]
