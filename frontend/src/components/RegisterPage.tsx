import { useForm, SubmitHandler } from "react-hook-form";
import { AuthResponse } from "../services/Login";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import FormCard from "./FormCard";

interface RegisterPageProps {
    onRegister: (username: string, password: string) => Promise<AuthResponse>;
};

interface RegisterFormInputs {
    email: string;
    password: string;
    confirm_password: string;
}

const RegisterPage: React.FC<RegisterPageProps> = ({onRegister}) => {
    const {register, handleSubmit, formState: {errors}} = useForm<RegisterFormInputs>();
    const navigate = useNavigate();
    const [error, setError] = useState<string>("");

    const onSubmit: SubmitHandler<RegisterFormInputs> = async (data) => {
        if (data.password != data.confirm_password) {
            setError("Passwords do not match");
            return;
        }

        try {
            await onRegister(data.email, data.password);
            navigate("/login"); // login page
        } catch (e) {
            console.error(e);
            setError(e instanceof Error ? e.message : "Something went wrong");
        }
    }

    return (
        <FormCard title="Register">
            <form onSubmit={handleSubmit(onSubmit)} className="register-form">
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

                <input
                    type="password"
                    {...register("confirm_password", {required: "Confirm password is required"})}
                    placeholder="Confirm password"
                />
                {errors.confirm_password && <p className="error-message">{errors.confirm_password.message}</p>}

                {errors && <p className="error-message">{error}</p>}

                <button type="submit">Register</button>
            </form>
        </FormCard>
    );
};

export default RegisterPage;