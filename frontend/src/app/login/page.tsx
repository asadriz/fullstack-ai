import { AppNav } from "@/components/app-nav";
import { AuthForm } from "@/components/auth-form";
import styles from "@/app/page.module.css";

export default function LoginPage() {
  return (
    <main className={styles.shell}>
      <AppNav />
      <section className={styles.panel}>
        <p className={styles.eyebrow}>Authentication</p>
        <h1>Login</h1>
        <p className={styles.muted}>
          Submit credentials to the Django REST Framework JWT login endpoint.
        </p>
        <AuthForm mode="login" />
      </section>
    </main>
  );
}
