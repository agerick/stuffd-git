import React, { Component } from "react";

class NutritionInfo extends Component {
  constructor(props) {
    super(props);
    this.renderObject = this.renderObject.bind(this);
  }

  nutrition_obj = this.props.nutrition_obj;

  renderObject(obj){
		return Object.entries(obj).map(([key, value], i) => {
			return (
				<div key={key}>
					id is: {value.id} ;
					name is: {value.name}
				</div>
			)
		})
	}

	render(){


  console.log('here is thing')
  console.log(this.props.nutrition_obj)
		return(
			<div>
      <h3> Nutrition Facts </h3>
				{this.props.nutrition_obj}
			</div>
		)
	}

}

export default NutritionInfo;
