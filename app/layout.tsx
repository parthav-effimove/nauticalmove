import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "nauticalmove | Maritime Commercial Intelligence",
  description:
    "nauticalmove provides maritime commercial intelligence across voyage estimation, cargo flows and fixtures for dry bulk and tanker markets.",
  openGraph: {
    title: "nauticalmove | Maritime Commercial Intelligence",
    description:
      "Maritime commercial intelligence for better decisions across dry bulk and tanker markets.",
    type: "website",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/nauticalmove-favicon.svg?v=2" type="image/svg+xml" />
      </head>
      <body>{children}</body>
    </html>
  );
}
