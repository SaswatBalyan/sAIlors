import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";

export default function HomePage() {
  return (
    <main className="min-h-dvh bg-bg text-white">
      <Navbar />
      <Hero />

      {/* Below hero you can keep your existing sections or link into the app */}
      <section
        id="about"
        className="mx-auto max-w-6xl px-4 py-16 text-white/80"
      >
        <h2 className="text-xl font-semibold mb-3">About sAIlor</h2>
        <p>
          sAIlor is an intelligent location analysis platform that leverages AI and 
          geospatial data to help entrepreneurs and businesses make informed decisions 
          about where to establish their ventures. Get started with our analysis tool.
        </p>
      </section>
    </main>
  );
}
