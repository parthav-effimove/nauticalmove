import type { Metadata } from "next";
import "./globals.css";

const siteTitle = "NauticalMove | Data & Analytics";
const siteDescription =
  "Maritime commercial intelligence for better decisions across dry bulk and tanker markets.";
const shareImage = "/opengraph-image";

export const metadata: Metadata = {
  metadataBase: new URL("https://www.nauticalmove.com"),
  title: { default: "NauticalMove | Data & Analytics", template: "%s | NauticalMove" },
  description:
    "Dry Bulk and Tanker tools for voyage calculations, cargo flows and fixture data.",
  openGraph: {
    title: "NauticalMove | Data & Analytics",
    description:
      "Dry Bulk and Tanker tools for voyage calculations, cargo flows and fixture data.",
    type: "website",
    siteName: "NauticalMove",
    images: [{ url: shareImage, width: 1200, height: 630, alt: "NauticalMove Dry Bulk and Tanker tools" }],
  },
  twitter: {
    card: "summary_large_image",
    title: siteTitle,
    description: siteDescription,
    images: [shareImage],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/nauticalmove-favicon.svg?v=3" type="image/svg+xml" />
      </head>
      <body>{children}</body>
    </html>
  );
}
