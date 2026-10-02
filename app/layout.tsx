import type { Metadata } from "next";
import "./globals.css";

const siteTitle = "nauticalmove | Maritime Commercial Intelligence";
const siteDescription =
  "Maritime commercial intelligence for better decisions across dry bulk and tanker markets.";
const shareImage = "/opengraph-image";

export const metadata: Metadata = {
  metadataBase: new URL("https://www.nauticalmove.com"),
  title: siteTitle,
  description:
    "nauticalmove provides maritime commercial intelligence across voyage estimation, cargo flows and fixtures for dry bulk and tanker markets.",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: siteTitle,
    description: siteDescription,
    url: "https://www.nauticalmove.com/",
    siteName: "nauticalmove",
    images: [
      {
        url: shareImage,
        width: 1200,
        height: 630,
        alt: "nauticalmove maritime commercial intelligence across global markets",
        type: "image/png",
      },
    ],
    type: "website",
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
