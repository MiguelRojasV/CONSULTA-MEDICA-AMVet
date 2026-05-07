import { createContext, useContext, useState, useEffect } from 'react'
import api from '../api/axios'
import React from 'react';

const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('amvet_token'))
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('amvet_user');
    return saved ? JSON.parse(saved) : null;
  });
  
  const [loading, setLoading] = useState(!user);

  useEffect(() => {
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      fetchMe()
    } else {
      setLoading(false)
    }
  }, [token])

  const fetchMe = async () => {
    try {
      // Ajustado para coincidir con el prefijo /api/auth del backend
      const res = await api.get('/api/auth/me') 
      setUser(res.data)
    } catch {
      logout()
    } finally {
      setLoading(false)
    }
  }

 const login = async (email, password) => {
  const res = await api.post('/auth/login', {
    email,
    password
  });

  const t = res.data.access_token;
  
  // 1. Preparamos el objeto de usuario
  const userData = {
    nombre: res.data.nombre,
    rol: res.data.rol,
    propietario_id: res.data.propietario_id
  };
localStorage.setItem('amvet_token', t);
  localStorage.setItem('amvet_user', JSON.stringify(userData)); // <-- AGREGA ESTA LÍNEA
  
  api.defaults.headers.common['Authorization'] = `Bearer ${t}`;
  
  // 3. ACTUALIZACIÓN DE ESTADOS
  setToken(t);
  setUser(userData);
  
  // Opcional: Forzar que loading sea false ya que ya tenemos al usuario
  setLoading(false); 
};
  const logout = () => {
    localStorage.removeItem('amvet_token')
    delete api.defaults.headers.common['Authorization']
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading, isAdmin: user?.rol === 'admin' }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)