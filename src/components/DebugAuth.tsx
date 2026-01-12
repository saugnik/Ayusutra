/**
 * Debug Component - Shows API Configuration
 * Temporary component to verify API settings
 */

import React, { useState } from 'react';
import apiClient from '../services/api';
import authService from '../services/auth.service';

const DebugAuth = () => {
    const [result, setResult] = useState<string>('');
    const [loading, setLoading] = useState(false);

    const testConnection = async () => {
        setLoading(true);
        setResult('Testing...');

        try {
            const response = await apiClient.get('/health');
            setResult(`✓ Backend Connected!\n${JSON.stringify(response.data, null, 2)}`);
        } catch (error: any) {
            setResult(`✗ Connection Failed:\n${error.message}\nURL: ${error.config?.baseURL}`);
        } finally {
            setLoading(false);
        }
    };

    const testRegister = async () => {
        setLoading(true);
        setResult('Registering...');

        try {
            const user = await authService.register({
                email: 'debug@test.com',
                full_name: 'Debug User',
                password: 'test123',
                role: 'patient',
                phone: '+1234567890'
            });
            setResult(`✓ Registration Success!\n${JSON.stringify(user, null, 2)}`);
        } catch (error: any) {
            setResult(`✗ Registration Failed:\n${error.response?.data?.detail || error.message}`);
        } finally {
            setLoading(false);
        }
    };

    const testLogin = async () => {
        setLoading(true);
        setResult('Logging in...');

        try {
            const token = await authService.login({
                email: 'debug@test.com',
                password: 'test123'
            });
            setResult(`✓ Login Success!\nToken: ${token.access_token.substring(0, 50)}...\nRole: ${token.role}`);
        } catch (error: any) {
            setResult(`✗ Login Failed:\n${error.response?.data?.detail || error.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'monospace' }}>
            <h2>🔧 API Debug Panel</h2>
            <p>API URL: {process.env.REACT_APP_API_URL || 'http://localhost:8001'}</p>

            <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
                <button onClick={testConnection} disabled={loading} style={buttonStyle}>
                    Test Connection
                </button>
                <button onClick={testRegister} disabled={loading} style={buttonStyle}>
                    Test Register
                </button>
                <button onClick={testLogin} disabled={loading} style={buttonStyle}>
                    Test Login
                </button>
            </div>

            <pre style={{
                marginTop: '20px',
                padding: '15px',
                background: '#f5f5f5',
                borderRadius: '5px',
                whiteSpace: 'pre-wrap'
            }}>
                {result || 'Click a button to test...'}
            </pre>
        </div>
    );
};

const buttonStyle = {
    padding: '10px 20px',
    background: '#2ba461',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer'
};

export default DebugAuth;
