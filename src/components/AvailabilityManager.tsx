
import React, { useState, useEffect } from 'react';
import { Plus, Trash2, Clock, MapPin, Save } from 'lucide-react';
import toast from 'react-hot-toast';
import { AvailabilitySchedule, AvailabilitySlot } from '../types/api.types';
import practitionerService from '../services/practitioner.service';

interface AvailabilityManagerProps {
    initialSchedule?: AvailabilitySchedule;
    onSave?: (schedule: AvailabilitySchedule) => void;
}

const DAYS_OF_WEEK = [
    { key: 'monday', label: 'Monday' },
    { key: 'tuesday', label: 'Tuesday' },
    { key: 'wednesday', label: 'Wednesday' },
    { key: 'thursday', label: 'Thursday' },
    { key: 'friday', label: 'Friday' },
    { key: 'saturday', label: 'Saturday' },
    { key: 'sunday', label: 'Sunday' },
];

const AvailabilityManager: React.FC<AvailabilityManagerProps> = ({ initialSchedule, onSave }) => {
    const [schedule, setSchedule] = useState<AvailabilitySchedule>({
        monday: [],
        tuesday: [],
        wednesday: [],
        thursday: [],
        friday: [],
        saturday: [],
        sunday: [],
    });

    const [selectedDay, setSelectedDay] = useState<keyof AvailabilitySchedule>('monday');
    const [newSlot, setNewSlot] = useState<AvailabilitySlot>({
        start_time: '09:00',
        end_time: '17:00',
        location: 'Main Clinic'
    });
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        if (initialSchedule && Object.keys(initialSchedule).length > 0) {
            // Ensure all days are present even if initialSchedule is partial
            setSchedule(prev => ({ ...prev, ...initialSchedule }));
        } else {
            loadProfile();
        }
    }, [initialSchedule]);

    const loadProfile = async () => {
        try {
            const profile = await practitionerService.getProfile();
            if (profile.availability_schedule && Object.keys(profile.availability_schedule).length > 0) {
                setSchedule(prev => ({ ...prev, ...profile.availability_schedule }));
            }
        } catch (error) {
            console.error("Failed to load profile", error);
        }
    };

    const handleAddSlot = () => {
        if (!newSlot.start_time || !newSlot.end_time || !newSlot.location) {
            toast.error("Please fill in all fields");
            return;
        }

        if (newSlot.start_time >= newSlot.end_time) {
            toast.error("End time must be after start time");
            return;
        }

        const updatedSchedule = {
            ...schedule,
            [selectedDay]: [...schedule[selectedDay], newSlot]
        };

        setSchedule(updatedSchedule);
        toast.success("Slot added");
    };

    const handleRemoveSlot = (index: number) => {
        const updatedDaySlots = [...schedule[selectedDay]];
        updatedDaySlots.splice(index, 1);

        setSchedule({
            ...schedule,
            [selectedDay]: updatedDaySlots
        });
    };

    const handleSaveSchedule = async () => {
        setIsLoading(true);
        try {
            await practitionerService.updateProfile({ availability_schedule: schedule });
            toast.success("Availability schedule saved successfully!");
            if (onSave) onSave(schedule);
        } catch (error) {
            console.error("Failed to save schedule", error);
            toast.error("Failed to save schedule.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 p-6">
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white">Availability Manager</h2>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Manage your weekly schedule and locations.</p>
                </div>
                <button
                    onClick={handleSaveSchedule}
                    disabled={isLoading}
                    className="flex items-center px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors font-medium disabled:opacity-50"
                >
                    <Save className="h-4 w-4 mr-2" />
                    {isLoading ? 'Saving...' : 'Save Changes'}
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                {/* Day Selection */}
                <div className="space-y-2">
                    <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Select Day</label>
                    {DAYS_OF_WEEK.map((day) => (
                        <button
                            key={day.key}
                            onClick={() => setSelectedDay(day.key as keyof AvailabilitySchedule)}
                            className={`w-full text-left px-4 py-3 rounded-lg transition-all flex justify-between items-center ${selectedDay === day.key
                                    ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 border border-primary-200 dark:border-primary-800 font-medium'
                                    : 'bg-gray-50 dark:bg-gray-700/50 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                                }`}
                        >
                            <span>{day.label}</span>
                            {schedule[day.key as keyof AvailabilitySchedule]?.length > 0 && (
                                <span className="bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-400 text-xs px-2 py-0.5 rounded-full font-bold">
                                    {schedule[day.key as keyof AvailabilitySchedule].length}
                                </span>
                            )}
                        </button>
                    ))}
                </div>

                {/* Slots Management */}
                <div className="md:col-span-3 space-y-6">
                    {/* Add New Slot */}
                    <div className="bg-gray-50 dark:bg-gray-750 p-4 rounded-lg border border-gray-200 dark:border-gray-600">
                        <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-3 flex items-center">
                            <Plus className="h-4 w-4 mr-1" /> Add New Slot for <span className="text-primary-600 dark:text-primary-400 ml-1 capitalize">{selectedDay}</span>
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
                            <div>
                                <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Start Time</label>
                                <div className="relative">
                                    <Clock className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                                    <input
                                        type="time"
                                        value={newSlot.start_time}
                                        onChange={(e) => setNewSlot({ ...newSlot, start_time: e.target.value })}
                                        className="pl-9 w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm p-2"
                                    />
                                </div>
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">End Time</label>
                                <div className="relative">
                                    <Clock className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                                    <input
                                        type="time"
                                        value={newSlot.end_time}
                                        onChange={(e) => setNewSlot({ ...newSlot, end_time: e.target.value })}
                                        className="pl-9 w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm p-2"
                                    />
                                </div>
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Location</label>
                                <div className="relative">
                                    <MapPin className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                                    <input
                                        type="text"
                                        value={newSlot.location || ''}
                                        onChange={(e) => setNewSlot({ ...newSlot, location: e.target.value })}
                                        placeholder="e.g. Main Clinic"
                                        className="pl-9 w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm p-2"
                                    />
                                </div>
                            </div>
                        </div>
                        <button
                            onClick={handleAddSlot}
                            className="mt-3 w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-primary-700 bg-primary-100 hover:bg-primary-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                        >
                            <Plus className="h-4 w-4 mr-1" /> Add Slot
                        </button>
                    </div>

                    {/* Existing Slots List */}
                    <div>
                        <h3 className="text-md font-medium text-gray-900 dark:text-white mb-3">
                            Scheduled Slots ({schedule[selectedDay]?.length || 0})
                        </h3>

                        {schedule[selectedDay]?.length === 0 ? (
                            <div className="text-center py-8 bg-white dark:bg-gray-800 rounded-lg border border-dashed border-gray-300 dark:border-gray-600">
                                <Clock className="mx-auto h-8 w-8 text-gray-400" />
                                <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">No slots configured for {selectedDay}.</p>
                            </div>
                        ) : (
                            <div className="space-y-3">
                                {schedule[selectedDay]?.map((slot, index) => (
                                    <div key={index} className="flex items-center justify-between p-4 bg-white dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600 shadow-sm hover:shadow-md transition-shadow">
                                        <div className="flex items-center space-x-6">
                                            <div className="flex items-center text-gray-900 dark:text-white font-medium">
                                                <Clock className="h-4 w-4 text-primary-500 mr-2" />
                                                {slot.start_time} - {slot.end_time}
                                            </div>
                                            <div className="flex items-center text-gray-500 dark:text-gray-300 text-sm">
                                                <MapPin className="h-4 w-4 text-gray-400 mr-1" />
                                                {slot.location}
                                            </div>
                                        </div>
                                        <button
                                            onClick={() => handleRemoveSlot(index)}
                                            className="text-red-500 hover:text-red-700 p-1.5 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-full transition-colors"
                                            title="Remove Slot"
                                        >
                                            <Trash2 className="h-4 w-4" />
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AvailabilityManager;
