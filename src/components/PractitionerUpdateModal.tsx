import React, { useState } from 'react';
import { X, Save } from 'lucide-react';
import { healthService } from '../services/health.service';
import { HealthLogCreate } from '../types/api.types';
import toast from 'react-hot-toast';

interface PractitionerUpdateModalProps {
    isOpen: boolean;
    onClose: () => void;
    patientId: number;
    patientName: string;
}

const PractitionerUpdateModal: React.FC<PractitionerUpdateModalProps> = ({ isOpen, onClose, patientId, patientName }) => {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState<HealthLogCreate>({
        patient_id: patientId,
        dosha_vata: 0,
        dosha_pitta: 0,
        dosha_kapha: 0,
        sleep_score: 75,
        stress_level: 'Medium',
        hydration: 2.0,
        notes: '',
        recommendations: ''
    });

    if (!isOpen) return null;

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            await healthService.createLog({ ...formData, patient_id: patientId });
            toast.success('Health record updated successfully!');
            onClose();
        } catch (error) {
            console.error('Error updating health record:', error);
            toast.error('Failed to update record.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 z-50 overflow-y-auto">
            <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div className="fixed inset-0 transition-opacity" aria-hidden="true">
                    <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
                </div>

                <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

                <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                    <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                        <div className="flex justify-between items-start">
                            <h3 className="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                                Update Health Status: {patientName}
                            </h3>
                            <button onClick={onClose} className="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none">
                                <X className="h-6 w-6" />
                            </button>
                        </div>

                        <form onSubmit={handleSubmit} className="mt-4 space-y-4">
                            {/* Dosha Sliders */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Dosha Balance (0-100)</label>
                                <div className="grid grid-cols-3 gap-4 mt-2">
                                    <div>
                                        <span className="text-xs text-blue-600 font-bold">Vata ({formData.dosha_vata})</span>
                                        <input
                                            type="range" min="0" max="100"
                                            value={formData.dosha_vata}
                                            onChange={(e) => setFormData({ ...formData, dosha_vata: parseInt(e.target.value) })}
                                            className="w-full h-2 bg-blue-100 rounded-lg appearance-none cursor-pointer"
                                        />
                                    </div>
                                    <div>
                                        <span className="text-xs text-red-600 font-bold">Pitta ({formData.dosha_pitta})</span>
                                        <input
                                            type="range" min="0" max="100"
                                            value={formData.dosha_pitta}
                                            onChange={(e) => setFormData({ ...formData, dosha_pitta: parseInt(e.target.value) })}
                                            className="w-full h-2 bg-red-100 rounded-lg appearance-none cursor-pointer"
                                        />
                                    </div>
                                    <div>
                                        <span className="text-xs text-green-600 font-bold">Kapha ({formData.dosha_kapha})</span>
                                        <input
                                            type="range" min="0" max="100"
                                            value={formData.dosha_kapha}
                                            onChange={(e) => setFormData({ ...formData, dosha_kapha: parseInt(e.target.value) })}
                                            className="w-full h-2 bg-green-100 rounded-lg appearance-none cursor-pointer"
                                        />
                                    </div>
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Sleep Score (0-100)</label>
                                    <input
                                        type="number"
                                        value={formData.sleep_score}
                                        onChange={(e) => setFormData({ ...formData, sleep_score: parseInt(e.target.value) })}
                                        className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm border p-2"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Stress Level</label>
                                    <select
                                        value={formData.stress_level}
                                        onChange={(e) => setFormData({ ...formData, stress_level: e.target.value })}
                                        className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm border p-2"
                                    >
                                        <option>Low</option>
                                        <option>Medium</option>
                                        <option>High</option>
                                    </select>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700">Dr. Recommendations / Notes</label>
                                <textarea
                                    rows={3}
                                    value={formData.recommendations}
                                    onChange={(e) => setFormData({ ...formData, recommendations: e.target.value })}
                                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm border p-2"
                                    placeholder="Enter advice for the patient..."
                                ></textarea>
                            </div>

                            <div className="mt-5 sm:mt-6">
                                <button
                                    type="submit"
                                    disabled={loading}
                                    className="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:text-sm disabled:opacity-50"
                                >
                                    {loading ? 'Saving...' : 'Update Patient Record'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PractitionerUpdateModal;
