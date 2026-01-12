
import React, { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { X, Calendar, Clock, User, FileText, Check, Award, DollarSign, ChevronRight } from 'lucide-react';
import appointmentService, { Practitioner } from '../services/appointment.service';
import { useAuth } from '../hooks/useAuth';

interface BookAppointmentModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void;
}

const BookAppointmentModal: React.FC<BookAppointmentModalProps> = ({ isOpen, onClose, onSuccess }) => {
    const { user } = useAuth();
    const [isLoading, setIsLoading] = useState(false);
    const [practitioners, setPractitioners] = useState<Practitioner[]>([]);

    // Form State
    const [step, setStep] = useState(1); // 1: Select Doctor, 2: Details
    const [selectedPractitionerId, setSelectedPractitionerId] = useState<number | null>(null);
    const [therapyType, setTherapyType] = useState('Consultation');
    const [date, setDate] = useState('');
    const [time, setTime] = useState('');
    const [notes, setNotes] = useState('');

    useEffect(() => {
        if (isOpen) {
            loadPractitioners();
            setStep(1); // Reset step on open
        }
    }, [isOpen]);

    const loadPractitioners = async () => {
        try {
            const data = await appointmentService.getAllPractitioners();
            setPractitioners(data);
        } catch (error) {
            console.error("Failed to load practitioners", error);
            toast.error("Could not load practitioners list.");
        }
    };

    const handleNextStep = () => {
        if (step === 1 && !selectedPractitionerId) {
            toast.error("Please select a practitioner first.");
            return;
        }
        setStep(2);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!selectedPractitionerId || !date || !time) {
            toast.error("Please fill in all required fields.");
            return;
        }

        setIsLoading(true);
        try {
            const dateTime = new Date(`${date}T${time}:00`).toISOString();

            await appointmentService.createAppointment({
                patient_id: user?.id || 0,
                practitioner_id: selectedPractitionerId,
                therapy_type: therapyType,
                scheduled_datetime: dateTime,
                duration_minutes: 60,
                notes: notes
            });

            toast.success("Appointment booked successfully!");
            onSuccess();
            onClose();
            // Reset form
            setSelectedPractitionerId(null);
            setDate('');
            setTime('');
            setNotes('');
            setStep(1);
        } catch (error: any) {
            toast.error(error.response?.data?.detail || "Failed to book appointment.");
        } finally {
            setIsLoading(false);
        }
    };

    if (!isOpen) return null;

    const selectedDoc = practitioners.find(p => p.id === selectedPractitionerId);

    return (
        <div className="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
            <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                {/* Background overlay */}
                <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" onClick={onClose}></div>

                <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

                <div className="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
                    {/* Header */}
                    <div className="bg-primary-50 px-6 py-4 border-b border-primary-100 flex justify-between items-center">
                        <div>
                            <h3 className="text-xl font-bold text-gray-900" id="modal-title">
                                {step === 1 ? 'Choose Your Practitioner' : 'Finalize Booking'}
                            </h3>
                            <p className="text-sm text-primary-600 mt-1">
                                Step {step} of 2: {step === 1 ? 'Select a specialized doctor' : 'Schedule your session'}
                            </p>
                        </div>
                        <button onClick={onClose} className="text-gray-400 hover:text-gray-500 bg-white rounded-full p-1 hover:bg-gray-100 transition-colors">
                            <X className="h-6 w-6" />
                        </button>
                    </div>

                    <div className="px-6 py-6 max-h-[70vh] overflow-y-auto">
                        {step === 1 ? (
                            // Step 1: Practitioner Selection Grid
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {practitioners.map(p => (
                                    <div
                                        key={p.id}
                                        onClick={() => setSelectedPractitionerId(p.id)}
                                        className={`relative border-2 rounded-xl p-4 cursor-pointer transition-all duration-200 hover:shadow-md ${selectedPractitionerId === p.id
                                                ? 'border-primary-500 bg-primary-50 ring-2 ring-primary-200'
                                                : 'border-gray-200 hover:border-primary-300'
                                            }`}
                                    >
                                        <div className="flex items-start space-x-4">
                                            <div className="flex-shrink-0">
                                                <div className="h-16 w-16 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 font-bold text-xl border-2 border-white shadow-sm">
                                                    {p.user?.full_name?.charAt(0) || 'D'}
                                                </div>
                                            </div>
                                            <div className="flex-1 min-w-0">
                                                <div className="flex justify-between items-start">
                                                    <h4 className="text-lg font-bold text-gray-900 truncate">
                                                        {p.user?.full_name || `Doctor #${p.id}`}
                                                    </h4>
                                                    {selectedPractitionerId === p.id && (
                                                        <Check className="h-6 w-6 text-primary-600" />
                                                    )}
                                                </div>
                                                <p className="text-sm text-primary-600 font-medium mb-2">{p.qualification || 'Certified Practitioner'}</p>

                                                <div className="flex flex-wrap gap-2 mb-3">
                                                    {p.specializations.map((spec, i) => (
                                                        <span key={i} className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-white border border-gray-200 text-gray-800">
                                                            {spec}
                                                        </span>
                                                    ))}
                                                </div>

                                                <div className="flex items-center justify-between text-sm text-gray-500 mt-2">
                                                    <div className="flex items-center">
                                                        <Award className="h-4 w-4 mr-1 text-yellow-500" />
                                                        <span>{p.experience_years} Years Exp.</span>
                                                    </div>
                                                    <div className="flex items-center font-semibold text-gray-900">
                                                        <DollarSign className="h-4 w-4 mr-1 text-green-500" />
                                                        <span>₹{p.consultation_fee}</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            // Step 2: Booking Details Form
                            <div className="space-y-6">
                                {/* Selected Doctor Summary */}
                                <div className="bg-blue-50 border border-blue-100 rounded-lg p-4 flex items-center justify-between">
                                    <div className="flex items-center space-x-3">
                                        <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold">
                                            {selectedDoc?.user?.full_name?.charAt(0)}
                                        </div>
                                        <div>
                                            <p className="text-sm text-blue-900 font-medium">Booking with</p>
                                            <p className="text-md font-bold text-blue-700">{selectedDoc?.user?.full_name}</p>
                                        </div>
                                    </div>
                                    <button onClick={() => setStep(1)} className="text-sm text-blue-600 hover:text-blue-800 font-medium underline">
                                        Change
                                    </button>
                                </div>

                                <form id="booking-form" onSubmit={handleSubmit} className="space-y-5">
                                    {/* Therapy Type */}
                                    <div>
                                        <label className="block text-sm font-semibold text-gray-700 mb-2">Therapy Type</label>
                                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                                            {['Consultation', 'Panchakarma', 'Abhyanga'].map((type) => (
                                                <div
                                                    key={type}
                                                    onClick={() => setTherapyType(type)}
                                                    className={`cursor-pointer text-center px-4 py-3 rounded-lg border font-medium transition-all ${therapyType === type
                                                            ? 'bg-primary-600 text-white border-primary-600 shadow-sm'
                                                            : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                                                        }`}
                                                >
                                                    {type}
                                                </div>
                                            ))}
                                            <select
                                                value={therapyType}
                                                onChange={(e) => setTherapyType(e.target.value)}
                                                className="sm:col-span-3 mt-2 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
                                            >
                                                <option value="Consultation">General Consultation</option>
                                                <option value="Panchakarma">Panchakarma Therapy</option>
                                                <option value="Abhyanga">Abhyanga (Oil Massage)</option>
                                                <option value="Shirodhara">Shirodhara</option>
                                                <option value="Follow-up">Follow-up Session</option>
                                            </select>
                                        </div>
                                    </div>

                                    {/* Date & Time */}
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        <div>
                                            <label className="block text-sm font-semibold text-gray-700 mb-2">Select Date</label>
                                            <div className="relative">
                                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                    <Calendar className="h-5 w-5 text-gray-400" />
                                                </div>
                                                <input
                                                    type="date"
                                                    value={date}
                                                    onChange={(e) => setDate(e.target.value)}
                                                    className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                                                    required
                                                    min={new Date().toISOString().split('T')[0]}
                                                />
                                            </div>
                                        </div>
                                        <div>
                                            <label className="block text-sm font-semibold text-gray-700 mb-2">Select Time</label>
                                            <div className="relative">
                                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                    <Clock className="h-5 w-5 text-gray-400" />
                                                </div>
                                                <input
                                                    type="time"
                                                    value={time}
                                                    onChange={(e) => setTime(e.target.value)}
                                                    className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                                                    required
                                                />
                                            </div>
                                        </div>
                                    </div>

                                    {/* Notes */}
                                    <div>
                                        <label className="block text-sm font-semibold text-gray-700 mb-2">Notes for Doctor (Optional)</label>
                                        <textarea
                                            value={notes}
                                            onChange={(e) => setNotes(e.target.value)}
                                            rows={3}
                                            className="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-lg p-3"
                                            placeholder="Describe your symptoms or reason for visit..."
                                        />
                                    </div>
                                </form>
                            </div>
                        )}
                    </div>

                    {/* Footer Actions */}
                    <div className="bg-gray-50 px-6 py-4 border-t border-gray-200 flex justify-between items-center">
                        {step === 2 && (
                            <button
                                type="button"
                                onClick={() => setStep(1)}
                                className="text-gray-600 font-medium hover:text-gray-900 px-4 py-2"
                            >
                                Back
                            </button>
                        )}
                        <div className="flex-1 flex justify-end">
                            {step === 1 ? (
                                <button
                                    type="button"
                                    onClick={handleNextStep}
                                    disabled={!selectedPractitionerId}
                                    className={`inline-flex items-center px-6 py-3 border border-transparent rounded-lg shadow-sm text-base font-medium text-white ${selectedPractitionerId
                                            ? 'bg-primary-600 hover:bg-primary-700 focus:ring-2 focus:ring-offset-2 focus:ring-primary-500'
                                            : 'bg-gray-300 cursor-not-allowed'
                                        }`}
                                >
                                    Next Step
                                    <ChevronRight className="ml-2 h-5 w-5" />
                                </button>
                            ) : (
                                <button
                                    form="booking-form"
                                    type="submit"
                                    disabled={isLoading}
                                    className="inline-flex items-center px-6 py-3 border border-transparent rounded-lg shadow-sm text-base font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 w-full md:w-auto justify-center"
                                >
                                    {isLoading ? 'Processing...' : 'Confirm Booking'}
                                    {!isLoading && <Check className="ml-2 h-5 w-5" />}
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BookAppointmentModal;
