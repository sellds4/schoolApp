var Child = require('./Child.jsx');

var Parent = React.createClass({
  render: function(){
    return (
	    <div>
	    	<form>
	    		<input type="text" name="firstName">
	    		<input type="text" name="lastName">
	    		<input type="email" name="email">
	    		<input type="password" name="password">
	    	</form>
	        <div> This is the parent. </div>
	        <Child name="child"/>
	    </div>
    )
  }
});

module.exports = Parent;
