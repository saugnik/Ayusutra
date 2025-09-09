import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const WelcomeIntro = () => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(0);
  const [isVisible, setIsVisible] = useState(true);

  const welcomeSteps = [
    {
      icon: "🙏",
      text: "Namaste",
      subtext: "Welcome to AyurSutra"
    },
    {
      icon: "🌿",
      text: "Traditional Wisdom",
      subtext: "5000 years of Ayurvedic knowledge"
    },
    {
      icon: "🤖",
      text: "AI-Powered",
      subtext: "Modern technology for better care"
    },
    {
      icon: "आ",
      text: "AyurSutra",
      subtext: "Your Digital Panchakarma Companion"
    }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentStep(prev => {
        if (prev < welcomeSteps.length - 1) {
          return prev + 1;
        } else {
          // After showing all steps, wait a bit then redirect
          setTimeout(() => {
            setIsVisible(false);
            setTimeout(() => {
              navigate('/home');
            }, 500);
          }, 2000);
          return prev;
        }
      });
    }, 1500);

    return () => clearInterval(timer);
  }, [navigate]);

  if (!isVisible) {
    return (
      <div className="fixed inset-0 bg-gradient-to-br from-primary-600 to-secondary-600 flex items-center justify-center z-50 opacity-0 transition-opacity duration-500">
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-gradient-to-br from-primary-600 to-secondary-600 flex items-center justify-center z-50">
      <div className="text-center text-white">
        <div className="mb-8 transform transition-all duration-1000 ease-in-out">
          <div className="text-8xl mb-6 animate-bounce">
            {welcomeSteps[currentStep].icon}
          </div>
        </div>
        
        <div className="space-y-4 animate-pulse">
          <h1 className="text-4xl lg:text-6xl font-bold font-serif mb-4 transform transition-all duration-500">
            {welcomeSteps[currentStep].text}
          </h1>
          <p className="text-xl lg:text-2xl text-primary-100 max-w-md mx-auto transform transition-all duration-500">
            {welcomeSteps[currentStep].subtext}
          </p>
        </div>

        <div className="mt-12 flex justify-center space-x-2">
          {welcomeSteps.map((_, index) => (
            <div
              key={index}
              className={`h-2 w-2 rounded-full transition-all duration-300 ${
                index <= currentStep ? 'bg-white' : 'bg-white/30'
              }`}
            />
          ))}
        </div>

        <div className="mt-8 text-sm text-primary-200 animate-pulse">
          Preparing your personalized experience...
        </div>
      </div>

    </div>
  );
};

export default WelcomeIntro;
