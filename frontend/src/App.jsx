import Hero from './components/HeroSection'
import FeaturesSection from './components/FeaturesSection'
import EventsSection from './components/EventsSection'
import InstallSection from './components/InstallSection'
import UsageSection from './components/UsageSection'
import Footer from './components/Footer'

function App() {
  return (
    <div className="bg-black min-h-screen">
      <Hero />
      <FeaturesSection />
      <EventsSection />
      <InstallSection />
      <UsageSection />
      <Footer />
    </div>
  )
}

export default App