"use client";

import { FormEvent, useState } from "react";
import { backend_request } from "@/lib/api";
import styles from "@/app/page.module.css";

type AuthMode = "login" | "signup";

type AuthFormProps = {
  mode: AuthMode;
};

export function AuthForm({ mode }: AuthFormProps) {
  const [email, set_email] = useState("");
  const [password, set_password] = useState("");
  const [confirm_password, set_confirm_password] = useState("");
  const [message, set_message] = useState("");
  const [is_loading, set_is_loading] = useState(false);

  const is_signup = mode === "signup";

  async function handle_submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    set_is_loading(true);
    set_message("");

    try {
      const payload: Record<string, string> = is_signup
        ? { email, password, confirm_password }
        : { email, password };
      const response = await backend_request(
        is_signup ? "/auth/signup/" : "/auth/token/",
        {
          body: payload,
          method: "POST",
        },
      );
      set_message(JSON.stringify(response, null, 2));
    } catch (error) {
      set_message(error instanceof Error ? error.message : "Request failed");
    } finally {
      set_is_loading(false);
    }
  }

  return (
    <form className={styles.form} onSubmit={handle_submit}>
      <label>
        Email
        <input
          autoComplete="email"
          name="email"
          onChange={(event) => set_email(event.target.value)}
          placeholder="user@example.com"
          required
          type="email"
          value={email}
        />
      </label>
      <label>
        Password
        <input
          autoComplete={is_signup ? "new-password" : "current-password"}
          minLength={8}
          name="password"
          onChange={(event) => set_password(event.target.value)}
          placeholder="At least 8 characters"
          required
          type="password"
          value={password}
        />
      </label>
      {is_signup ? (
        <label>
          Confirm password
          <input
            autoComplete="new-password"
            minLength={8}
            name="confirm_password"
            onChange={(event) => set_confirm_password(event.target.value)}
            placeholder="Repeat password"
            required
            type="password"
            value={confirm_password}
          />
        </label>
      ) : null}

      <button disabled={is_loading} type="submit">
        {is_loading ? "Sending..." : is_signup ? "Create account" : "Login"}
      </button>

      {message ? <pre className={styles.response}>{message}</pre> : null}
    </form>
  );
}
