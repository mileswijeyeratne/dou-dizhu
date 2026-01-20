import React from "react";

import "./FormCard.css";

interface FormCardProps {
    title: string;
    children: React.ReactNode;
}

const FormCard: React.FC<FormCardProps> = ({title, children}) => {
    return (
        <div className="form-page">
            <div className="form-card">
                <h1>{title}</h1>
                {children}
            </div>
        </div>
    )
}

export default FormCard;