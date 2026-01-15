import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Calendar,
  Bell,
  Activity,
  Shield,
  Users,
  TrendingUp,
  CheckCircle,
  Star,
  Menu,
  X,
  ChevronDown,
  MessageCircle,
  Phone,
  Mail
} from 'lucide-react';

const LandingPage = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [openFAQ, setOpenFAQ] = useState<number | null>(null);

  const features = [
    {
      icon: Calendar,
      title: "Automated Therapy Scheduling",
      description: "AI-powered scheduling system that automatically plans and manages therapy sessions based on patient needs and practitioner availability."
    },
    {
      icon: Bell,
      title: "Smart Notifications",
      description: "Personalized alerts for pre and post-procedure precautions via SMS, email, and in-app notifications."
    },
    {
      icon: Activity,
      title: "Real-Time Therapy Tracking",
      description: "Monitor therapy progress with live tracking, personalized recovery milestones, and visual progress indicators."
    },
    {
      icon: TrendingUp,
      title: "Feedback & Analytics",
      description: "Comprehensive patient feedback system with data analytics to optimize treatment outcomes."
    },
    {
      icon: Users,
      title: "Multi-Role Management",
      description: "Seamlessly manage patients, practitioners, and administrators with role-based access control."
    },
    {
      icon: Shield,
      title: "Security & Compliance",
      description: "HIPAA-compliant platform ensuring complete data security and regulatory compliance."
    }
  ];

  const howItWorks = [
    {
      step: 1,
      title: "Patient Intake",
      description: "Comprehensive digital onboarding with medical history, consent management, and personalized therapy planning.",
      icon: "👤"
    },
    {
      step: 2,
      title: "Therapy Management",
      description: "Automated scheduling, real-time tracking, and integrated feedback loops throughout the therapy process.",
      icon: "🧘‍♀️"
    },
    {
      step: 3,
      title: "Follow-up & Analytics",
      description: "Continuous monitoring, progress analytics, and data-driven insights for optimal patient outcomes.",
      icon: "📊"
    }
  ];

  const testimonials = [
    {
      name: "Dr. Priya Sharma",
      role: "Ayurvedic Practitioner",
      content: "AyurSutra has revolutionized how we manage our Panchakarma treatments. The automated scheduling and patient tracking features have increased our efficiency by 60%.",
      rating: 5,
      clinic: "Vedic Wellness Center"
    },
    {
      name: "Rajesh Kumar",
      role: "Patient",
      content: "The notification system and progress tracking made my Virechana therapy so much easier to follow. I knew exactly what to do before and after each session.",
      rating: 5,
      clinic: "Patient"
    },
    {
      name: "Dr. Ananya Reddy",
      role: "Clinic Administrator",
      content: "Managing 50+ patients daily is now seamless. The platform's analytics help us optimize our operations and improve patient satisfaction significantly.",
      rating: 5,
      clinic: "Ayush Healing Center"
    }
  ];

  const aiAgents = [
    {
      name: "Patient Assistant Agent",
      role: "Your Personal Therapy Guide",
      description: "Answers patient questions about therapies, provides pre/post-care instructions, and offers 24/7 support using advanced NLP and Ayurvedic knowledge base.",
      icon: "🤖",
      bgColor: "bg-blue-100",
      iconColor: "text-blue-600",
      capabilities: ["Therapy Q&A", "Care Instructions", "24/7 Support"]
    },
    {
      name: "Smart Scheduling Agent",
      role: "Intelligent Appointment Manager",
      description: "Manages appointments based on patient preferences, medical conditions, and practitioner availability using AI-powered optimization algorithms.",
      icon: "📅",
      bgColor: "bg-green-100",
      iconColor: "text-green-600",
      capabilities: ["Smart Booking", "Conflict Resolution", "Preference Learning"]
    },
    {
      name: "Feedback Analyzer Agent",
      role: "Sentiment & Insight Processor",
      description: "Processes and categorizes patient feedback, identifies improvement areas, and generates actionable insights for better treatment outcomes.",
      icon: "📊",
      bgColor: "bg-purple-100",
      iconColor: "text-purple-600",
      capabilities: ["Sentiment Analysis", "Pattern Recognition", "Quality Insights"]
    },
    {
      name: "Practitioner Support Agent",
      role: "Clinical Decision Assistant",
      description: "Generates comprehensive reports, provides clinical insights, and assists doctors with data-driven treatment recommendations.",
      icon: "👨‍⚕️",
      bgColor: "bg-orange-100",
      iconColor: "text-orange-600",
      capabilities: ["Report Generation", "Clinical Insights", "Decision Support"]
    }
  ];

  const faqs = [
    {
      question: "What is Panchakarma and how does AyurSutra help?",
      answer: "Panchakarma is a traditional Ayurvedic detoxification and rejuvenation therapy. AyurSutra digitalizes the entire process, from scheduling to progress tracking, ensuring authentic traditional treatments with modern efficiency."
    },
    {
      question: "Is the platform HIPAA compliant?",
      answer: "Yes, AyurSutra is fully HIPAA compliant with end-to-end encryption, secure data storage, and comprehensive audit trails to protect patient information."
    },
    {
      question: "Can I integrate AyurSutra with my existing clinic management system?",
      answer: "Yes, we provide REST APIs and integration support for most popular clinic management systems. Our team assists with seamless data migration."
    },
    {
      question: "What kind of support do you provide?",
      answer: "We offer 24/7 technical support, comprehensive training for your staff, regular software updates, and dedicated customer success management."
    }
  ];

  return (
    <div className="min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100">
      {/* Navigation */}
      <nav className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-100 dark:border-gray-800 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-xl">आ</span>
                </div>
                <span className="ml-3 text-2xl font-bold text-gray-900 dark:text-white">AyurSutra</span>
              </div>
            </Link>

            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-8">
                <a href="#features" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 text-sm font-medium">Features</a>
                <a href="#how-it-works" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 text-sm font-medium">How It Works</a>
                <Link to="/map" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 text-sm font-medium">Find Clinics</Link>
                <a href="#testimonials" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 text-sm font-medium">Testimonials</a>
                <a href="#agents" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 text-sm font-medium">AI Agents</a>
                <a href="#faq" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 text-sm font-medium">FAQ</a>
              </div>
            </div>

            <div className="hidden md:flex items-center space-x-4">
              <Link to="/auth" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 text-sm font-medium">
                Sign In
              </Link>
              <Link to="/auth" className="btn-primary">
                Get Started
              </Link>
            </div>

            <div className="md:hidden">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="text-gray-700 dark:text-gray-300 hover:text-primary-600 p-2"
              >
                {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
              </button>
            </div>
          </div>

          {/* Mobile menu */}
          {isMenuOpen && (
            <div className="md:hidden">
              <div className="px-2 pt-2 pb-3 space-y-1 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
                <a href="#features" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 block px-3 py-2 text-base font-medium">Features</a>
                <a href="#how-it-works" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 block px-3 py-2 text-base font-medium">How It Works</a>
                <a href="#testimonials" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 block px-3 py-2 text-base font-medium">Testimonials</a>
                <a href="#agents" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 block px-3 py-2 text-base font-medium">AI Agents</a>
                <a href="#faq" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 block px-3 py-2 text-base font-medium">FAQ</a>
                <Link to="/auth" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 block px-3 py-2 text-base font-medium">Sign In</Link>
                <Link to="/auth" className="block px-3 py-2">
                  <span className="btn-primary inline-block">Get Started</span>
                </Link>
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-50 via-white to-secondary-50 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950 py-20 lg:py-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="text-center lg:text-left">
              <div className="mb-4">
                <span className="inline-block px-4 py-2 bg-primary-100 dark:bg-primary-900/40 text-primary-800 dark:text-primary-300 rounded-full text-sm font-medium mb-6">
                  🌿 Traditional Wisdom Meets Modern Technology
                </span>
              </div>
              <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 dark:text-white leading-tight">
                Digital <span className="text-primary-600 dark:text-primary-400">Panchakarma</span> Management Platform
              </h1>
              <p className="mt-6 text-xl text-gray-600 dark:text-gray-400 leading-relaxed">
                Transform your Ayurvedic practice with our comprehensive digital solution.
                From automated scheduling to real-time therapy tracking, AyurSutra bridges
                5000 years of traditional wisdom with cutting-edge healthcare technology.
              </p>
              <div className="mt-6 flex items-center space-x-6 text-sm text-gray-600 dark:text-gray-400">
                <div className="flex items-center">
                  <span className="text-primary-600 dark:text-primary-400 font-bold text-lg mr-2">500+</span>
                  <span>Active Practitioners</span>
                </div>
                <div className="flex items-center">
                  <span className="text-primary-600 dark:text-primary-400 font-bold text-lg mr-2">10K+</span>
                  <span>Patients Served</span>
                </div>
                <div className="flex items-center">
                  <span className="text-primary-600 dark:text-primary-400 font-bold text-lg mr-2">50+</span>
                  <span>Therapy Centers</span>
                </div>
              </div>
              <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <Link to="/auth?role=patient" className="btn-primary text-center">
                  Sign Up as Patient
                </Link>
                <Link to="/auth?role=practitioner" className="btn-secondary text-center">
                  Sign Up as Practitioner
                </Link>
                <button className="bg-white dark:bg-gray-800 text-primary-600 dark:text-primary-400 border-2 border-primary-600 dark:border-primary-500 px-6 py-3 rounded-lg font-medium hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors duration-200">
                  Request Demo
                </button>
              </div>

              <div className="mt-12 flex items-center justify-center lg:justify-start space-x-8 text-sm text-gray-600 dark:text-gray-400">
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-primary-500 dark:text-primary-400 mr-2" />
                  <span>HIPAA Compliant</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-primary-500 dark:text-primary-400 mr-2" />
                  <span>24/7 Support</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-primary-500 dark:text-primary-400 mr-2" />
                  <span>Free Trial</span>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 transform rotate-3 hover:rotate-0 transition-transform duration-500 border border-gray-100 dark:border-gray-700">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Next Session</h3>
                    <span className="bg-primary-100 dark:bg-primary-900/40 text-primary-800 dark:text-primary-300 px-3 py-1 rounded-full text-sm">Today</span>
                  </div>
                  <div className="border-l-4 border-primary-500 dark:border-primary-400 pl-4">
                    <p className="font-medium text-gray-900 dark:text-white">Virechana Therapy</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Dr. Priya Sharma • 2:00 PM</p>
                  </div>
                  <div className="bg-accent-50 dark:bg-accent-900/20 p-4 rounded-lg">
                    <h4 className="font-medium text-gray-900 dark:text-white mb-2">Pre-procedure Checklist</h4>
                    <div className="space-y-2">
                      <div className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 dark:text-green-400 mr-2" />
                        <span className="text-sm text-gray-600 dark:text-gray-400">Fasting completed</span>
                      </div>
                      <div className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 dark:text-green-400 mr-2" />
                        <span className="text-sm text-gray-600 dark:text-gray-400">Meditation done</span>
                      </div>
                      <div className="flex items-center">
                        <div className="h-4 w-4 border-2 border-gray-300 dark:border-gray-600 rounded mr-2"></div>
                        <span className="text-sm text-gray-600 dark:text-gray-400">Arrive 30 minutes early</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white dark:bg-gray-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white">
              Comprehensive Panchakarma Management
            </h2>
            <p className="mt-4 text-xl text-gray-600 dark:text-gray-400">
              Everything you need to modernize traditional Ayurvedic treatments
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="card hover:shadow-xl transition-shadow duration-300">
                <div className="flex items-center mb-4">
                  <div className="bg-primary-100 dark:bg-primary-900/30 p-3 rounded-lg">
                    <feature.icon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
                  </div>
                  <h3 className="ml-4 text-xl font-semibold text-gray-900 dark:text-white">{feature.title}</h3>
                </div>
                <p className="text-gray-600 dark:text-gray-400 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white">
              How AyurSutra Works
            </h2>
            <p className="mt-4 text-xl text-gray-600 dark:text-gray-400">
              Three simple steps to transform your Panchakarma practice
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {howItWorks.map((step, index) => (
              <div key={index} className="text-center">
                <div className="relative mb-8">
                  <div className="w-20 h-20 bg-primary-600 rounded-full flex items-center justify-center text-4xl mx-auto transform transition-transform hover:scale-110">
                    {step.icon}
                  </div>
                  <div className="absolute -top-2 -right-2 bg-secondary-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold shadow-lg">
                    {step.step}
                  </div>
                  {index < howItWorks.length - 1 && (
                    <div className="hidden md:block absolute top-10 left-full w-full h-0.5 bg-primary-200 dark:bg-primary-800 transform -translate-x-10"></div>
                  )}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">{step.title}</h3>
                <p className="text-gray-600 dark:text-gray-400 leading-relaxed">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-20 bg-white dark:bg-gray-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white">
              Trusted by Healthcare Professionals
            </h2>
            <p className="mt-4 text-xl text-gray-600 dark:text-gray-400">
              See what our users are saying about AyurSutra
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="card">
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-600 dark:text-gray-300 mb-6 italic">"{testimonial.content}"</p>
                <div className="border-t border-gray-100 dark:border-gray-700 pt-4">
                  <div className="font-semibold text-gray-900 dark:text-white">{testimonial.name}</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">{testimonial.role}</div>
                  <div className="text-sm text-primary-600 dark:text-primary-400">{testimonial.clinic}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* AI Agents Section */}
      <section id="agents" className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white">
              Powered by Intelligent AI Agents
            </h2>
            <p className="mt-4 text-xl text-gray-600 dark:text-gray-400">
              Four specialized AI agents working together with LangGraph coordination
            </p>
            <div className="mt-6 inline-flex items-center px-4 py-2 bg-primary-100 dark:bg-primary-900/40 rounded-full text-primary-800 dark:text-primary-300">
              <span className="text-sm font-medium">🧠 Built with LangGraph Architecture</span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {aiAgents.map((agent, index) => (
              <div key={index} className="card hover:shadow-xl transition-all duration-300 group">
                <div className="flex items-start space-x-4">
                  <div className={`${agent.bgColor} dark:bg-opacity-10 p-4 rounded-xl flex-shrink-0 group-hover:scale-110 transition-transform duration-300`}>
                    <div className={`text-3xl ${agent.iconColor}`}>{agent.icon}</div>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">{agent.name}</h3>
                    <p className="text-primary-600 dark:text-primary-400 font-medium mb-3">{agent.role}</p>
                    <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed mb-4">{agent.description}</p>

                    <div className="space-y-2">
                      <p className="text-xs font-medium text-gray-500 dark:text-gray-500 uppercase tracking-wide">Key Capabilities:</p>
                      <div className="flex flex-wrap gap-2">
                        {agent.capabilities.map((capability, capIndex) => (
                          <span
                            key={capIndex}
                            className="px-3 py-1 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-full text-xs font-medium"
                          >
                            {capability}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="text-center mt-12">
            <div className="card max-w-4xl mx-auto">
              <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">Agent Architecture Overview</h3>
              <p className="text-gray-600 dark:text-gray-400 mb-6 leading-relaxed">
                Our AI agents are orchestrated using <strong>LangGraph</strong>, ensuring seamless communication
                and coordination between specialized agents. Each agent focuses on specific tasks while
                contributing to the overall patient care ecosystem.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
                <div className="text-center">
                  <div className="w-12 h-12 bg-primary-100 dark:bg-primary-900/30 rounded-lg flex items-center justify-center mx-auto mb-3">
                    <span className="text-xl">🔄</span>
                  </div>
                  <h4 className="font-semibold text-gray-900 dark:text-white">Coordinated Workflow</h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Agents work together seamlessly</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-primary-100 dark:bg-primary-900/30 rounded-lg flex items-center justify-center mx-auto mb-3">
                    <span className="text-xl">⚡</span>
                  </div>
                  <h4 className="font-semibold text-gray-900 dark:text-white">Real-time Processing</h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Instant responses and updates</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-primary-100 dark:bg-primary-900/30 rounded-lg flex items-center justify-center mx-auto mb-3">
                    <span className="text-xl">🎯</span>
                  </div>
                  <h4 className="font-semibold text-gray-900 dark:text-white">Specialized Focus</h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Each agent excels in its domain</p>
                </div>
              </div>
              <div className="mt-8">
                <Link to="/auth" className="btn-primary">
                  Experience AI-Powered Healthcare
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="py-20 bg-white dark:bg-gray-950">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white">
              Frequently Asked Questions
            </h2>
            <p className="mt-4 text-xl text-gray-600 dark:text-gray-400">
              Everything you need to know about AyurSutra
            </p>
          </div>

          <div className="space-y-4">
            {faqs.map((faq, index) => (
              <div key={index} className="bg-white dark:bg-gray-900 rounded-lg shadow-sm border border-gray-200 dark:border-gray-800">
                <button
                  className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                  onClick={() => setOpenFAQ(openFAQ === index ? null : index)}
                >
                  <span className="font-medium text-gray-900 dark:text-white">{faq.question}</span>
                  <ChevronDown className={`h-5 w-5 text-gray-500 transform transition-transform ${openFAQ === index ? 'rotate-180' : ''
                    }`} />
                </button>
                {openFAQ === index && (
                  <div className="px-6 pb-4">
                    <p className="text-gray-600 dark:text-gray-400 leading-relaxed">{faq.answer}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary-600 to-primary-700">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl lg:text-4xl font-bold text-white mb-8">
            Ready to Transform Your Panchakarma Practice?
          </h2>
          <p className="text-xl text-primary-100 mb-10">
            Join hundreds of practitioners already using AyurSutra to deliver better patient outcomes
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/auth" className="bg-white text-primary-600 px-8 py-4 rounded-lg font-semibold hover:bg-primary-50 transition-colors duration-200">
              Start Free Trial
            </Link>
            <button className="bg-transparent text-white border-2 border-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-primary-600 transition-colors duration-200">
              Schedule Demo
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="md:col-span-2">
              <Link to="/" className="flex items-center mb-4">
                <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-xl">आ</span>
                </div>
                <span className="ml-3 text-2xl font-bold">AyurSutra</span>
              </Link>
              <p className="text-gray-400 mb-6 max-w-md">
                Bridging traditional Ayurvedic wisdom with modern digital healthcare technology
                for better patient outcomes and streamlined practice management.
              </p>
              <div className="flex space-x-4">
                <Phone className="h-5 w-5 text-gray-400" />
                <span className="text-gray-400">+91 98765 43210</span>
              </div>
              <div className="flex space-x-4 mt-2">
                <Mail className="h-5 w-5 text-gray-400" />
                <span className="text-gray-400">hello@ayursutra.com</span>
              </div>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#features" className="hover:text-white">Features</a></li>
                <li><a href="#" className="hover:text-white">Pricing</a></li>
                <li><a href="#" className="hover:text-white">API Documentation</a></li>
                <li><a href="#" className="hover:text-white">Integrations</a></li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#faq" className="hover:text-white">FAQ</a></li>
                <li><a href="#" className="hover:text-white">Help Center</a></li>
                <li><a href="#" className="hover:text-white">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white">Terms of Service</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
            <p>&copy; 2024 AyurSutra. All rights reserved. | Made with ❤️ for Ayurvedic Healthcare</p>
          </div>
        </div>
      </footer>

      {/* Chat Widget */}
      <div className="fixed bottom-6 right-6 z-50">
        <button className="bg-primary-600 text-white p-4 rounded-full shadow-lg hover:bg-primary-700 transition-colors duration-200">
          <MessageCircle className="h-6 w-6" />
        </button>
      </div>
    </div>
  );
};

export default LandingPage;
