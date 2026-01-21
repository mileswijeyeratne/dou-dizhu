import React, { createContext, useContext, useState, useEffect } from "react";

interface AuthContextType {
    isLoggedIn: boolean;
    email: string | null;
    setLoggedIn: (loggedIn: boolean, email?: string) => void;
    logout: () => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
    children: React.ReactNode;
};

export const AuthProvider: React.FC<AuthProviderProps> = ({children}) => {
    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
    const [email, setEmail] = useState<string | null>(null);

    useEffect(() => {
        const storedEmail = localStorage.getItem("email");
        if (storedEmail) {
            setIsLoggedIn(true);
            setEmail(storedEmail);
        }
    }, []);

    const handleSetLoggedIn = (loggedIn: boolean, userEmail?: string) => {
        setIsLoggedIn(loggedIn);
        if (loggedIn && userEmail) {
            console.log("set email")
            setEmail(userEmail);
            localStorage.setItem("email", userEmail);
        } else {
            setEmail(null);
            localStorage.removeItem("email");
        }
    };

    const handleLogout = () => {
        setIsLoggedIn(false);
        setEmail(null);
        localStorage.removeItem("email");
        localStorage.removeItem("playerName");
    }

    return <AuthContext.Provider value={{
        isLoggedIn,
        email,
        setLoggedIn: handleSetLoggedIn,
        logout: handleLogout,
    }}>
        {children}
    </AuthContext.Provider>
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
};