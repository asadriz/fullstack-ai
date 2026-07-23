import { AppNav } from "@/components/app-nav";
import { AuthForm } from "@/components/auth-form";
import styles from "@/app/page.module.css";

export default function SignupPage() {
  return (
    <main className={styles.shell}>
      <AppNav />
      <section className={styles.panel}>
        <p className={styles.eyebrow}>Authentication</p>
        <h1>Signup</h1>
        <p className={styles.muted}>
          Create a user through the backend signup endpoint and receive tokens.
        </p>
        <AuthForm mode="signup" />
      </section>
    </main>
  );
}
