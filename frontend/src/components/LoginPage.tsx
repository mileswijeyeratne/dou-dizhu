import { useForm, SubmitHandler } from "react-hook-form";
import { AuthResponse } from "../services/Login";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import FormCard from "./FormCard";
import { useAuth } from "../services/AuthContext";

interface LoginPageProps {
    onLogin: (username: string, password: string) => Promise<AuthResponse>;
};

interface LoginFormInputs {
    email: string;
    password: string;
}

const LoginPage: React.FC<LoginPageProps> = ({onLogin}) => {
    const {register, handleSubmit, formState: {errors}} = useForm<LoginFormInputs>();
    const navigate = useNavigate();
    const { setLoggedIn } = useAuth();
    const [error, setError] = useState<string>("");

    const onSubmit: SubmitHandler<LoginFormInputs> = async (data) => {
        try {
            await onLogin(data.email, data.password);
            console.log(data)
            console.log(data.email)
            setLoggedIn(true, data.email);
            navigate("/"); // landing page
        } catch (e) {
            console.error(e);
            setError(e instanceof Error ? e.message : "Something went wrong");
        }
    }

    return (
        <FormCard title="Login">
            <form onSubmit={handleSubmit(onSubmit)} className="login-form">
                <input
                    type="email"
                    {...register("email", {required: "Email is required"})}
                    placeholder="Email"
                />
                {errors.email && <p className="error-message">{errors.email.message}</p>}
                
                <input
                    type="password"
                    {...register("password", {required: "Password is required"})}
                    placeholder="Password"
                />
                {errors.password && <p className="error-message">{errors.password.message}</p>}

                {errors && <p className="error-message">{error}</p>}

                <button type="submit">Login</button>

                <Link to="/register">Don't have an account? Register</Link>
            </form>
        </FormCard>
    );
};

export default LoginPage;