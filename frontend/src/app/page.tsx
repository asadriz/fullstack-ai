import Link from "next/link";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.shell}>
        <div className={styles.hero}>
          <p className={styles.eyebrow}>Next.js + Django REST Framework</p>
          <h1>Frontend boilerplate connected to the backend API.</h1>
          <p>
            This React app includes starter flows for login, signup, and a live
            backend health check.
          </p>
        </div>

        <div className={styles.grid}>
          <Link className={styles.cardLink} href="/login">
            <span>Login</span>
            <small>Authenticate with `/auth/token/`.</small>
          </Link>
          <Link className={styles.cardLink} href="/signup">
            <span>Signup</span>
            <small>Create a user with `/auth/signup/`.</small>
          </Link>
          <Link className={styles.cardLink} href="/health">
            <span>Health check</span>
            <small>Verify `/healthcheck/` from the browser.</small>
          </Link>
        </div>
      </main>
    </div>
  );
}
