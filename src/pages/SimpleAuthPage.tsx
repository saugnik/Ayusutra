import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import toast, { Toaster } from 'react-hot-toast';
import { Mail, Lock, User, Phone, Building, FileText } from 'lucide-react';

const SimpleAuthPage = () => {
    const navigate = useNavigate();
    const { login, register } = useAuth();
    const [isLogin, setIsLogin] = useState(true);
    const [isLoading, setIsLoading] = useState(false);

    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirmPassword: '',
        fullName: '',
        phone: '',
        role: 'patient' as 'patient' | 'practitioner' | 'admin',
        licenseNumber: '',
        specializations: '',
        clinicName: ''
    });

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            if (isLogin) {
                await login({
                    email: formData.email,
                    password: formData.password
                });

                toast.success('Login successful!');

                const storedUser = localStorage.getItem('user');
                if (storedUser) {
                    const user = JSON.parse(storedUser);
                    if (user.role === 'patient') {
                        navigate('/patient');
                    } else if (user.role === 'practitioner') {
                        navigate('/practitioner');
                    } else if (user.role === 'admin') {
                        navigate('/admin');
                    }
                }
            } else {
                if (formData.password !== formData.confirmPassword) {
                    toast.error('Passwords do not match');
                    setIsLoading(false);
                    return;
                }

                if (!formData.fullName || !formData.email || !formData.password) {
                    toast.error('Please fill in all required fields');
                    setIsLoading(false);
                    return;
                }

                const registerData: any = {
                    email: formData.email,
                    full_name: formData.fullName,
                    password: formData.password,
                    role: formData.role,
                    phone: formData.phone || undefined
                };

                if (formData.role === 'practitioner') {
                    registerData.license_number = formData.licenseNumber || undefined;
                    registerData.specializations = formData.specializations
                        ? formData.specializations.split(',').map(s => s.trim())
                        : undefined;
                    registerData.clinic_name = formData.clinicName || undefined;
                }

                await register(registerData);

                toast.success('Registration successful! Please login.');
                setIsLogin(true);
                setFormData({
                    email: formData.email,
                    password: '',
                    confirmPassword: '',
                    fullName: '',
                    phone: '',
                    role: 'patient',
                    licenseNumber: '',
                    specializations: '',
                    clinicName: ''
                });
            }
        } catch (error: any) {
            console.error('Authentication Error Details:', {
                message: error.message,
                response: error.response,
                status: error.response?.status,
                data: error.response?.data,
                config: error.config
            });

            const errorMessage = error.response?.data?.detail || error.message || 'Authentication failed. Please try again.';
            toast.error(errorMessage);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
            <Toaster position="top-right" />
            <div className="min-h-screen bg-dashboard bg-gradient-to-br from-primary-50 via-white to-secondary-50 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
                <div className="max-w-md w-full space-y-8">
                    <div>
                        <Link to="/home" className="flex justify-center">
                            <div className="w-16 h-16 bg-primary-600 rounded-xl flex items-center justify-center">
                                <span className="text-3xl">🌿</span>
                            </div>
                        </Link>
                        <h2 className="mt-6 text-center text-3xl font-bold text-gray-900 dark:text-white">
                            {isLogin ? 'Welcome back' : 'Create your account'}
                        </h2>
                        <p className="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
                            {isLogin ? "Don't have an account? " : 'Already have an account? '}
                            <button
                                onClick={() => setIsLogin(!isLogin)}
                                className="font-medium text-primary-600 dark:text-primary-400 hover:text-primary-500"
                            >
                                {isLogin ? 'Sign up' : 'Sign in'}
                            </button>
                        </p>
                    </div>

                    <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                        <div className="rounded-md shadow-sm space-y-4">
                            {!isLogin && (
                                <>
                                    <div>
                                        <label htmlFor="fullName" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                            Full Name *
                                        </label>
                                        <div className="relative">
                                            <User className="absolute left-3 top-3 h-5 w-5 text-gray-400 dark:text-gray-500" />
                                            <input
                                                id="fullName"
                                                name="fullName"
                                                type="text"
                                                required={!isLogin}
                                                value={formData.fullName}
                                                onChange={handleInputChange}
                                                className="input-field pl-10"
                                                placeholder="John Doe"
                                            />
                                        </div>
                                    </div>

                                    <div>
                                        <label htmlFor="role" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                            I am a *
                                        </label>
                                        <select
                                            id="role"
                                            name="role"
                                            value={formData.role}
                                            onChange={handleInputChange}
                                            className="input-field"
                                            required={!isLogin}
                                        >
                                            <option value="patient">Patient</option>
                                            <option value="practitioner">Practitioner</option>
                                            <option value="admin">Administrator</option>
                                        </select>
                                    </div>
                                </>
                            )}

                            <div>
                                <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                    Email Address *
                                </label>
                                <div className="relative">
                                    <Mail className="absolute left-3 top-3 h-5 w-5 text-gray-400 dark:text-gray-500" />
                                    <input
                                        id="email"
                                        name="email"
                                        type="email"
                                        required
                                        value={formData.email}
                                        onChange={handleInputChange}
                                        className="input-field pl-10"
                                        placeholder="you@example.com"
                                    />
                                </div>
                            </div>

                            {!isLogin && (
                                <div>
                                    <label htmlFor="phone" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                        Phone Number
                                    </label>
                                    <div className="relative">
                                        <Phone className="absolute left-3 top-3 h-5 w-5 text-gray-400 dark:text-gray-500" />
                                        <input
                                            id="phone"
                                            name="phone"
                                            type="tel"
                                            value={formData.phone}
                                            onChange={handleInputChange}
                                            className="input-field pl-10"
                                            placeholder="+91 98765 43210"
                                        />
                                    </div>
                                </div>
                            )}

                            {!isLogin && formData.role === 'practitioner' && (
                                <>
                                    <div>
                                        <label htmlFor="licenseNumber" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                            License Number
                                        </label>
                                        <div className="relative">
                                            <FileText className="absolute left-3 top-3 h-5 w-5 text-gray-400 dark:text-gray-500" />
                                            <input
                                                id="licenseNumber"
                                                name="licenseNumber"
                                                type="text"
                                                value={formData.licenseNumber}
                                                onChange={handleInputChange}
                                                className="input-field pl-10"
                                                placeholder="LIC123456"
                                            />
                                        </div>
                                    </div>

                                    <div>
                                        <label htmlFor="specializations" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                            Specializations (comma-separated)
                                        </label>
                                        <input
                                            id="specializations"
                                            name="specializations"
                                            type="text"
                                            value={formData.specializations}
                                            onChange={handleInputChange}
                                            className="input-field"
                                            placeholder="Panchakarma, Ayurveda"
                                        />
                                    </div>

                                    <div>
                                        <label htmlFor="clinicName" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                            Clinic Name
                                        </label>
                                        <div className="relative">
                                            <Building className="absolute left-3 top-3 h-5 w-5 text-gray-400 dark:text-gray-500" />
                                            <input
                                                id="clinicName"
                                                name="clinicName"
                                                type="text"
                                                value={formData.clinicName}
                                                onChange={handleInputChange}
                                                className="input-field pl-10"
                                                placeholder="Wellness Clinic"
                                            />
                                        </div>
                                    </div>
                                </>
                            )}

                            <div>
                                <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                    Password *
                                </label>
                                <div className="relative">
                                    <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400 dark:text-gray-500" />
                                    <input
                                        id="password"
                                        name="password"
                                        type="password"
                                        required
                                        value={formData.password}
                                        onChange={handleInputChange}
                                        className="input-field pl-10"
                                        placeholder="••••••••"
                                    />
                                </div>
                            </div>

                            {!isLogin && (
                                <div>
                                    <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                        Confirm Password *
                                    </label>
                                    <div className="relative">
                                        <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400 dark:text-gray-500" />
                                        <input
                                            id="confirmPassword"
                                            name="confirmPassword"
                                            type="password"
                                            required={!isLogin}
                                            value={formData.confirmPassword}
                                            onChange={handleInputChange}
                                            className="input-field pl-10"
                                            placeholder="••••••••"
                                        />
                                    </div>
                                </div>
                            )}
                        </div>

                        <div>
                            <button
                                type="submit"
                                disabled={isLoading}
                                className="btn-primary w-full"
                            >
                                {isLoading ? 'Please wait...' : (isLogin ? 'Sign in' : 'Create account')}
                            </button>
                        </div>

                        {isLogin && (
                            <div className="text-center">
                                <Link to="/home" className="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-500">
                                    Back to home
                                </Link>
                            </div>
                        )}
                    </form>
                </div>
            </div>
        </>
    );
};

export default SimpleAuthPage;
