import { Metadata } from "next";
import "../styles/globals.css";

let title = "Physicks";
let description = "Physics made easy";
let ogimage = "/landing.png";
let sitename = "";

export const metadata: Metadata = {
  title,
  description,
  icons: {
    icon: "/physics_logo.png",
  },
  openGraph: {
    images: [ogimage],
    title,
    description,
    url: "",
    siteName: sitename,
    locale: "en_US",
    type: "website",
  },

};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-white text-black">{children}</body>
    </html>
  );
}
