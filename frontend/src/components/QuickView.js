import React, { Component } from "react";
import { findDOMNode } from "react-dom";
import NutritionInfo from "./NutritionInfo";
import QuickScrollBar from "./QuickScrollBar";


class QuickView extends Component {
  constructor(props) {
    super(props);
    this.renderObject = this.renderObject.bind(this);
  }

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


  componentDidMount() {
    document.addEventListener(
      "click",
      this.handleClickOutside.bind(this),
      true
    );
  }

  componentWillUnmount() {
    document.removeEventListener(
      "click",
      this.handleClickOutside.bind(this),
      true
    );
  }

  handleClickOutside(event) {
    const domNode = findDOMNode(this.refs.modal);
    if (!domNode || !domNode.contains(event.target)) {
      this.props.closeModal();
    }
  }

  handleClose() {
    this.props.closeModal();
  }

//rendering method!
  render() {
    // return statement!
    return (

      <div
        className={
          this.props.openModal ? "modal-wrapper active" : "modal-wrapper"
        }
      >
        <div className="modal" ref="modal">
          <button
            type="button"
            className="close"
            onClick={this.handleClose.bind(this)}
          >
            &times;
          </button>
          <div className="quick-view">
            <div className="quick-view-image">
              <img
                src={this.props.product.image}
                alt={this.props.product.name}
              />
            </div>
            <QuickScrollBar>
            <div className="quick-view-details">
              <span className="product-name">{this.props.product.name}</span>
              <span className="product-price">{this.props.product.price}</span>
              <div className="">Ready in: {(this.props.product.readyInMinutes)} minutes</div>
              <br/>

              <div className="instructions"><h3> Servings:</h3> <p> {this.props.product.servings} </p> </div>
              <div className="instructions"><h3> Instructions:</h3> <p> {this.props.product.instructions} </p> </div>
              <div className="instructions"><h3> Source Url:</h3> <p> {this.props.product.sourceUrl} </p> </div>
              <div className="instructions"><h3> Ingredients</h3> <p> {this.props.product.igd_list} </p> </div>
              <div className="instructions"><h3> Nutrition Facts</h3> <p> {this.props.product.nutrition} </p> </div>




              {console.log('Nutrition facts')}

              {console.log(this.props.product.nutrition)}

              {console.log('Ingredient facts')}
              {console.log(this.props.product.igd_list)}

              {console.log('Whole Object')}
              {console.log(this.props.product)}




            </div>
            </QuickScrollBar>
          </div>
        </div>
      </div>

    );
  }
}

export default QuickView;
