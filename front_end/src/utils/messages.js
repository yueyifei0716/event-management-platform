import React from 'react';
import ReactDOM from 'react-dom';
import Message from '../components/Confirmation/Message';

const message = {
    dom: null,
    success({ content, duration = 2000 }) {
        // Create a dom
        this.dom = document.createElement('div');
        // Defining Components
        const JSXdom = <Message content={content} duration={duration} type="success">{content}</Message>;
        // Rendering the DOM
        ReactDOM.render(JSXdom, this.dom);
        // Placed under the body node
        document.body.appendChild(this.dom);
    },
    // defined and used about error
    error({ content, duration = 2000 }) {
        this.dom = document.createElement('div');
        const JSXdom = <Message content={content} duration={duration} type="error"></Message>;
        ReactDOM.render(JSXdom, this.dom);
        document.body.appendChild(this.dom);
    },
    // throw a warning
    warning({ content, duration = 2000 }) {
        this.dom = document.createElement('div');
        const JSXdom = <Message content={content} duration={duration} type="warning"></Message>;
        ReactDOM.render(JSXdom, this.dom);
        document.body.appendChild(this.dom);
    },
    // throw a info
    info({ content, duration = 2000 }) {
        this.dom = document.createElement('div');
        const JSXdom = <Message content={content} duration={duration} type="warning"></Message>;
        ReactDOM.render(JSXdom, this.dom);
        document.body.appendChild(this.dom);
    }
};

export default message;