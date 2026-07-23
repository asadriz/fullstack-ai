import Link from "next/link";
import styles from "@/app/page.module.css";

export function AppNav() {
  return (
    <nav className={styles.nav}>
      <Link href="/">Home</Link>
      <Link href="/login">Login</Link>
      <Link href="/signup">Signup</Link>
      <Link href="/health">Health</Link>
    </nav>
  );
}
