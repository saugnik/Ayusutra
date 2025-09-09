import React, { useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { 
  User, 
  UserCheck, 
  Shield, 
  Phone, 
  Mail, 
  Lock, 
  Eye, 
  EyeOff,
  ArrowRight,
  CheckCircle,
  Upload,
  FileText
} from 'lucide-react';

const AuthPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [isLogin, setIsLogin] = useState(true);
  const [selectedRole, setSelectedRole] = useState(searchParams.get('role') || '');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  
  const [formData, setFormData] = useState({
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    dateOfBirth: '',
    gender: '',
    medicalConditions: [] as string[],
    allergies: '',
    emergencyContact: '',
    licenseNumber: '',
    specialization: [] as string[],
    clinicName: '',
    clinicAddress: '',
    experience: '',
    licenseFile: null as File | null
  });

  const [otpData, setOtpData] = useState({
    otp: '',
    method: 'email' as 'email' | 'phone'
  });

  const roles = [
    {
      id: 'patient',
      title: 'Patient',
      icon: User,
      description: 'Book appointments, track therapy progress, and manage your Panchakarma journey',
      color: 'primary'
    },
    {
      id: 'practitioner',
      title: 'Practitioner',
      icon: UserCheck,
      description: 'Manage patients, schedule therapies, and provide personalized Ayurvedic care',
      color: 'secondary'
    },
    {
      id: 'admin',
      title: 'Administrator',
      icon: Shield,
      description: 'Oversee clinic operations, manage staff, and access comprehensive analytics',
      color: 'accent'
    }
  ];

  const medicalConditions = [
    'Diabetes', 'Hypertension', 'Heart Disease', 'Arthritis', 
    'Thyroid Disorders', 'Digestive Issues', 'Respiratory Problems',
    'Skin Conditions', 'Mental Health', 'Other'
  ];

  const specializations = [
    'Panchakarma Specialist', 'Ayurvedic Physician', 'Pulse Diagnosis',
    'Herbal Medicine', 'Yoga Therapy', 'Meditation', 'Nadi Pariksha',
    'Abhyanga', 'Shirodhara', 'Basti', 'Virechana', 'Vamana'
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCheckboxChange = (value: string, field: 'medicalConditions' | 'specialization') => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].includes(value) 
        ? prev[field].filter(item => item !== value)
        : [...prev[field], value]
    }));
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setFormData(prev => ({
        ...prev,
        licenseFile: file
      }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (currentStep === 1) {
      // Move to OTP verification
      setCurrentStep(2);
    } else if (currentStep === 2) {
      // Verify OTP and move to profile setup
      setCurrentStep(3);
    } else if (currentStep === 3) {
      // Complete profile setup and navigate to appropriate dashboard
      if (selectedRole === 'patient') {
        navigate('/patient');
      } else if (selectedRole === 'practitioner') {
        navigate('/practitioner');
      } else if (selectedRole === 'admin') {
        navigate('/admin');
      }
    }
  };

  const renderRoleSelection = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Choose Your Role</h2>
        <p className="text-gray-600">Select how you'll be using AyurSutra</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {roles.map((role) => (
          <button
            key={role.id}
            onClick={() => setSelectedRole(role.id)}
            className={`p-6 rounded-xl border-2 transition-all duration-200 text-left ${
              selectedRole === role.id
                ? `border-${role.color}-500 bg-${role.color}-50`
                : 'border-gray-200 hover:border-gray-300 bg-white'
            }`}
          >
            <role.icon className={`h-8 w-8 mb-4 ${
              selectedRole === role.id ? `text-${role.color}-600` : 'text-gray-400'
            }`} />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">{role.title}</h3>
            <p className="text-sm text-gray-600">{role.description}</p>
          </button>
        ))}
      </div>
      
      {selectedRole && (
        <div className="flex justify-center mt-8">
          <button
            onClick={() => setCurrentStep(isLogin ? 2 : 1)}
            className="btn-primary flex items-center"
          >
            Continue as {roles.find(r => r.id === selectedRole)?.title}
            <ArrowRight className="ml-2 h-4 w-4" />
          </button>
        </div>
      )}
    </div>
  );

  const renderAuthForm = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          {isLogin ? 'Sign In' : 'Create Account'}
        </h2>
        <p className="text-gray-600">
          {isLogin ? 'Welcome back to AyurSutra' : 'Join the AyurSutra community'}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {!isLogin && (
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                First Name
              </label>
              <input
                type="text"
                name="firstName"
                value={formData.firstName}
                onChange={handleInputChange}
                className="input-field"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Last Name
              </label>
              <input
                type="text"
                name="lastName"
                value={formData.lastName}
                onChange={handleInputChange}
                className="input-field"
                required
              />
            </div>
          </div>
        )}

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Email Address
          </label>
          <div className="relative">
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              className="input-field pl-10"
              required
            />
            <Mail className="absolute left-3 top-3.5 h-4 w-4 text-gray-400" />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Phone Number
          </label>
          <div className="relative">
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleInputChange}
              className="input-field pl-10"
              placeholder="+91 98765 43210"
              required
            />
            <Phone className="absolute left-3 top-3.5 h-4 w-4 text-gray-400" />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Password
          </label>
          <div className="relative">
            <input
              type={showPassword ? "text" : "password"}
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              className="input-field pl-10 pr-10"
              required
            />
            <Lock className="absolute left-3 top-3.5 h-4 w-4 text-gray-400" />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-3.5 text-gray-400 hover:text-gray-600"
            >
              {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            </button>
          </div>
        </div>

        {!isLogin && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Confirm Password
            </label>
            <div className="relative">
              <input
                type={showConfirmPassword ? "text" : "password"}
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                className="input-field pl-10 pr-10"
                required
              />
              <Lock className="absolute left-3 top-3.5 h-4 w-4 text-gray-400" />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute right-3 top-3.5 text-gray-400 hover:text-gray-600"
              >
                {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
          </div>
        )}

        <button type="submit" className="btn-primary w-full">
          {isLogin ? 'Sign In' : 'Create Account'}
        </button>
      </form>

      <div className="text-center">
        <p className="text-gray-600">
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <button
            onClick={() => setIsLogin(!isLogin)}
            className="text-primary-600 hover:text-primary-700 font-medium"
          >
            {isLogin ? 'Sign up' : 'Sign in'}
          </button>
        </p>
      </div>
    </div>
  );

  const renderOTPVerification = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Verify Your Identity</h2>
        <p className="text-gray-600">
          We've sent a verification code to your {otpData.method === 'email' ? 'email' : 'phone'}
        </p>
      </div>

      <div className="flex justify-center space-x-2 mb-6">
        <button
          onClick={() => setOtpData(prev => ({ ...prev, method: 'email' }))}
          className={`px-4 py-2 rounded-lg font-medium ${
            otpData.method === 'email'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          Email
        </button>
        <button
          onClick={() => setOtpData(prev => ({ ...prev, method: 'phone' }))}
          className={`px-4 py-2 rounded-lg font-medium ${
            otpData.method === 'phone'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          SMS
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Verification Code
          </label>
          <input
            type="text"
            name="otp"
            value={otpData.otp}
            onChange={(e) => setOtpData(prev => ({ ...prev, otp: e.target.value }))}
            className="input-field text-center text-lg tracking-widest"
            placeholder="123456"
            maxLength={6}
            required
          />
        </div>

        <button type="submit" className="btn-primary w-full">
          Verify Code
        </button>
      </form>

      <div className="text-center">
        <p className="text-gray-600">
          Didn't receive the code?{' '}
          <button className="text-primary-600 hover:text-primary-700 font-medium">
            Resend
          </button>
        </p>
      </div>
    </div>
  );

  const renderProfileSetup = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Complete Your Profile</h2>
        <p className="text-gray-600">
          Help us personalize your AyurSutra experience
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {selectedRole === 'patient' && (
          <>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Date of Birth
                </label>
                <input
                  type="date"
                  name="dateOfBirth"
                  value={formData.dateOfBirth}
                  onChange={handleInputChange}
                  className="input-field"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Gender
                </label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleInputChange}
                  className="input-field"
                  required
                >
                  <option value="">Select Gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Medical Conditions (Check all that apply)
              </label>
              <div className="grid grid-cols-2 gap-2">
                {medicalConditions.map((condition) => (
                  <label key={condition} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.medicalConditions.includes(condition)}
                      onChange={() => handleCheckboxChange(condition, 'medicalConditions')}
                      className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                    <span className="ml-2 text-sm text-gray-700">{condition}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Allergies
              </label>
              <textarea
                name="allergies"
                value={formData.allergies}
                onChange={handleInputChange}
                className="input-field"
                rows={3}
                placeholder="Please list any known allergies..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Emergency Contact
              </label>
              <input
                type="tel"
                name="emergencyContact"
                value={formData.emergencyContact}
                onChange={handleInputChange}
                className="input-field"
                placeholder="+91 98765 43210"
                required
              />
            </div>
          </>
        )}

        {selectedRole === 'practitioner' && (
          <>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  License Number
                </label>
                <input
                  type="text"
                  name="licenseNumber"
                  value={formData.licenseNumber}
                  onChange={handleInputChange}
                  className="input-field"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Years of Experience
                </label>
                <input
                  type="number"
                  name="experience"
                  value={formData.experience}
                  onChange={handleInputChange}
                  className="input-field"
                  min="0"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Specializations (Check all that apply)
              </label>
              <div className="grid grid-cols-2 gap-2 max-h-40 overflow-y-auto">
                {specializations.map((specialization) => (
                  <label key={specialization} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.specialization.includes(specialization)}
                      onChange={() => handleCheckboxChange(specialization, 'specialization')}
                      className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                    <span className="ml-2 text-sm text-gray-700">{specialization}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Clinic Name
              </label>
              <input
                type="text"
                name="clinicName"
                value={formData.clinicName}
                onChange={handleInputChange}
                className="input-field"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Clinic Address
              </label>
              <textarea
                name="clinicAddress"
                value={formData.clinicAddress}
                onChange={handleInputChange}
                className="input-field"
                rows={3}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Upload License Document
              </label>
              <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:border-primary-400">
                <div className="space-y-1 text-center">
                  <Upload className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="flex text-sm text-gray-600">
                    <label className="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500">
                      <span>Upload a file</span>
                      <input
                        type="file"
                        onChange={handleFileUpload}
                        className="sr-only"
                        accept=".pdf,.jpg,.jpeg,.png"
                      />
                    </label>
                    <p className="pl-1">or drag and drop</p>
                  </div>
                  <p className="text-xs text-gray-500">PDF, PNG, JPG up to 10MB</p>
                  {formData.licenseFile && (
                    <div className="flex items-center justify-center mt-2">
                      <FileText className="h-4 w-4 text-green-500 mr-1" />
                      <span className="text-sm text-green-600">{formData.licenseFile.name}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </>
        )}

        {selectedRole === 'admin' && (
          <div className="text-center py-8">
            <Shield className="mx-auto h-16 w-16 text-primary-600 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Administrator Access Request
            </h3>
            <p className="text-gray-600 mb-6">
              Admin accounts require approval from our team. You'll receive an email once your request is reviewed.
            </p>
          </div>
        )}

        <button type="submit" className="btn-primary w-full">
          {selectedRole === 'admin' ? 'Submit Request' : 'Complete Setup'}
        </button>
      </form>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <Link to="/" className="flex justify-center items-center mb-8">
          <div className="w-12 h-12 bg-primary-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-2xl">आ</span>
          </div>
          <span className="ml-3 text-3xl font-bold text-gray-900">AyurSutra</span>
        </Link>
      </div>

      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow-xl rounded-lg sm:px-10">
          {/* Progress Steps */}
          {!selectedRole && (
            <div className="mb-8">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-medium">1</span>
                  </div>
                  <span className="ml-2 text-sm font-medium text-primary-600">Choose Role</span>
                </div>
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                    <span className="text-gray-500 text-sm font-medium">2</span>
                  </div>
                  <span className="ml-2 text-sm text-gray-500">Verify</span>
                </div>
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                    <span className="text-gray-500 text-sm font-medium">3</span>
                  </div>
                  <span className="ml-2 text-sm text-gray-500">Profile</span>
                </div>
              </div>
            </div>
          )}

          {selectedRole && currentStep > 0 && (
            <div className="mb-8">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                    <CheckCircle className="h-4 w-4 text-white" />
                  </div>
                  <span className="ml-2 text-sm font-medium text-primary-600">Role Selected</span>
                </div>
                <div className="flex items-center">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    currentStep >= 2 ? 'bg-primary-600' : 'bg-gray-200'
                  }`}>
                    {currentStep > 2 ? (
                      <CheckCircle className="h-4 w-4 text-white" />
                    ) : (
                      <span className={`text-sm font-medium ${
                        currentStep >= 2 ? 'text-white' : 'text-gray-500'
                      }`}>2</span>
                    )}
                  </div>
                  <span className={`ml-2 text-sm ${
                    currentStep >= 2 ? 'font-medium text-primary-600' : 'text-gray-500'
                  }`}>Verify</span>
                </div>
                <div className="flex items-center">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    currentStep >= 3 ? 'bg-primary-600' : 'bg-gray-200'
                  }`}>
                    <span className={`text-sm font-medium ${
                      currentStep >= 3 ? 'text-white' : 'text-gray-500'
                    }`}>3</span>
                  </div>
                  <span className={`ml-2 text-sm ${
                    currentStep >= 3 ? 'font-medium text-primary-600' : 'text-gray-500'
                  }`}>Profile</span>
                </div>
              </div>
            </div>
          )}

          {/* Render appropriate step */}
          {!selectedRole && renderRoleSelection()}
          {selectedRole && currentStep === 1 && renderAuthForm()}
          {selectedRole && currentStep === 2 && renderOTPVerification()}
          {selectedRole && currentStep === 3 && renderProfileSetup()}
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
