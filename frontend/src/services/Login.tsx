import { SERVER_URL } from '../assets/BackendURL';

interface RegisterRequest {
    email: string;
    password: string;
};

interface LoginRequest {
    email: string;
    password: string;
};

export interface AuthResponse {
    status: string;
    msg: string;
}

export async function tryRegister(email: string, password: string): Promise<AuthResponse> {
    const req: RegisterRequest = {email, password};

    const response = await fetch(`http://${SERVER_URL}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(req),
        credentials: "include",
    });

    if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || "Something went wrong");
    }

    return await response.json()
}

export async function tryLogin(email: string, password: string): Promise<AuthResponse> {
    const req: LoginRequest = {email, password};

    const response = await fetch(`http://${SERVER_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(req),
        credentials: 'include',
    });


    if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || "Something went wrong");
    }

    return await response.json();
}