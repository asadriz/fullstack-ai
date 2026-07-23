import { AppNav } from "@/components/app-nav";
import { HealthCheckCard } from "@/components/health-check-card";
import styles from "@/app/page.module.css";

export default function HealthPage() {
  return (
    <main className={styles.shell}>
      <AppNav />
      <section className={styles.panel}>
        <p className={styles.eyebrow}>Backend connection</p>
        <h1>Health check</h1>
        <p className={styles.muted}>
          Run a browser request against the backend `/healthcheck/` endpoint.
        </p>
        <HealthCheckCard />
      </section>
    </main>
  );
}
