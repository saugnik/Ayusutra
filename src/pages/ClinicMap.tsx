import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { Practitioner } from '../types/api.types';
import patientService from '../services/patient.service';
import L from 'leaflet';
import { MapPin, Phone, User, Calendar } from 'lucide-react';

// Fix Leaflet icon issue in React
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const ClinicMap: React.FC = () => {
    const [practitioners, setPractitioners] = useState<Practitioner[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchClinics = async () => {
            try {
                const data = await patientService.getAllPractitioners();
                // Filter practitioners with location data
                const validPractitioners = data.filter(p => p.latitude && p.longitude);
                setPractitioners(validPractitioners);
            } catch (error) {
                console.error("Failed to load clinics", error);
            } finally {
                setLoading(false);
            }
        };
        fetchClinics();
    }, []);

    // Default center (e.g. New Delhi or user location)
    const position: [number, number] = [28.6139, 77.2090];

    return (
        <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
            <header className="bg-white dark:bg-gray-800 shadow-sm border-b dark:border-gray-700 p-4 z-10">
                <div className="max-w-7xl mx-auto flex justify-between items-center">
                    <h1 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                        <MapPin className="text-primary-600" /> Clinic Locator
                    </h1>
                    <a href="/patient" className="text-primary-600 hover:text-primary-700 font-medium text-sm">
                        Back to Dashboard
                    </a>
                </div>
            </header>

            <div className="flex-1 relative">
                {loading ? (
                    <div className="absolute inset-0 flex items-center justify-center bg-gray-100 dark:bg-gray-900 z-0">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
                    </div>
                ) : (
                    <MapContainer center={position} zoom={12} scrollWheelZoom={true} style={{ height: '100%', width: '100%' }}>
                        <TileLayer
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        />
                        {practitioners.map(practitioner => (
                            <Marker
                                key={practitioner.id}
                                position={[practitioner.latitude!, practitioner.longitude!]}
                            >
                                <Popup>
                                    <div className="p-1 min-w-[200px]">
                                        <h3 className="font-bold text-lg text-primary-800 mb-1">{practitioner.clinic_name || "AyurSutra Clinic"}</h3>
                                        <p className="text-sm text-gray-600 font-medium mb-2 flex items-center gap-1">
                                            <User className="h-3 w-3" /> Dr. {practitioner.user?.full_name || `Practitioner #${practitioner.id}`}
                                        </p>
                                        <div className="text-xs text-gray-500 space-y-1 mb-3">
                                            <p>{practitioner.clinic_address}</p>
                                            <p className="flex items-center gap-1"><Phone className="h-3 w-3" /> {practitioner.user?.phone || 'Contact for details'}</p>
                                        </div>
                                        <button className="w-full py-1.5 bg-primary-600 text-white text-xs rounded hover:bg-primary-700 transition flex items-center justify-center gap-1">
                                            <Calendar className="h-3 w-3" /> Book Appointment
                                        </button>
                                    </div>
                                </Popup>
                            </Marker>
                        ))}
                    </MapContainer>
                )}
            </div>
        </div>
    );
};

export default ClinicMap;
