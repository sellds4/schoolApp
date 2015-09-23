var RegisterForm = React.createClass({
    render: function() {
        return (
            <div>
                <form className="registerForm" onSubmit={this.handleSubmit}>
                    <input type="text" name="firstName" placeholder="first name" ref="firstName" />
                    <input type="text" name="lastName" placeholder="last name" ref="lastName" />
                    <input type="email" name="email" placeholder="email" ref="email" />
                    <input type="password" name="password" placeholder="password" ref="password"/>
                    <button type="submit">Submit</button>
                </form>
            </div>
        )
    },
    handleSubmit: function(e) {
        e.preventDefault();
        var firstName = React.findDOMNode(this.refs.firstName).value.trim(),
            lastName = React.findDOMNode(this.refs.lastName).value.trim(),
            email = React.findDOMNode(this.refs.email).value.trim(),
            password = React.findDOMNode(this.refs.password).value.trim();

        if (!firstName || !lastName || !email || !password) {
            return;
        }
        this.regSubmit({first_name: firstName, last_name: lastName, email: email, password: password});
        return;
    },
    regSubmit: function(regData) {
        $.ajax({
            url: '/api/student',
            dataType: 'json',
            type: 'POST',
            data: regData,
            success: function(data) {
                this.setState({data: data});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    }
})

module.exports = RegisterForm;
