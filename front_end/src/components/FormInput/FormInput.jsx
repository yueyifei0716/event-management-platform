import { useState } from "react";
import React from "react";
import "./forminput.css";

const FormInput = (props) => {
    const [focused, setFocused] = useState(false);
    const { label, errorMessage, id, ...inputProps } = props;

    // check which input box is currently focused
    const handleFocus = () => {
        setFocused(true);
    };

    // a function to display all of the input boxes in a form by iteration
    return (
        <div className="formInput">
            <label>{label}</label>
            <input
                {...inputProps}
                onBlur={handleFocus}
                onFocus={() => {
                    if (inputProps.name === "confirmPassword") {
                        setFocused(true)
                    }
                }}
                focused={focused.toString()}
            />
            <span className="error">{errorMessage}</span>
        </div>
    );
};

export default FormInput;