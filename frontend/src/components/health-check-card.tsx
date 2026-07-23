"use client";

import { useState } from "react";
import { backend_request, backend_url } from "@/lib/api";
import styles from "@/app/page.module.css";

export function HealthCheckCard() {
  const [status, set_status] = useState("Not checked yet");
  const [is_loading, set_is_loading] = useState(false);

  async function check_health() {
    set_is_loading(true);

    try {
      const response = await backend_request("/healthcheck/");
      set_status(JSON.stringify(response, null, 2));
    } catch (error) {
      set_status(error instanceof Error ? error.message : "Request failed");
    } finally {
      set_is_loading(false);
    }
  }

  return (
    <section className={styles.panel}>
      <p className={styles.muted}>Backend URL: {backend_url}</p>
      <button disabled={is_loading} onClick={check_health} type="button">
        {is_loading ? "Checking..." : "Check backend health"}
      </button>
      <pre className={styles.response}>{status}</pre>
    </section>
  );
}
