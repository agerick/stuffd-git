import React, { Component } from "react";
import Product from "./Product";
import LoadingProducts from "../loaders/Products";
import NoResults from "../empty-states/NoResults";
import CSSTransitionGroup from "react-transition-group/CSSTransitionGroup";

class Products extends Component {
  constructor() {
    super();
  }
  render() {
    let productsData;
    let term = this.props.searchTerm;
    let isVegetarianOn = this.props.isVegetarianOn;
    let isGlutenOn = this.props.isGlutenOn;
    let isDairyOn = this.props.isDairyOn;
    let x;

    function searchingFor(term) {
      return function(x) {
        return x.name.toLowerCase().includes(term.toLowerCase()) || !term;
      };
    }
    function isVeggie(isVegetarianOn) {
      return (isVegetarianOn ? (x)=>x.vegetarian : (x)=>true);
    };
    function isDairy(isDairyOn) {
      return (isDairyOn ? (x)=>x.dairyFree : (x)=>true);
    };
    function isGluten(isGlutenOn) {
      return (isGlutenOn ? (x)=>x.glutenFree : (x)=>true);
    };


    // below determines which products to show
    // as we loop through this array passed to us
    // from props!
    // the array is this.props.productsList
    productsData = this.props.productsList
      .filter(searchingFor(term))
      .filter(isVeggie(isVegetarianOn))
      .filter(isDairy(isDairyOn))
      .filter(isGluten(isGlutenOn))
      .map(product => {
        return (
          <Product
            key={product.id}
            price={product.price}
            name={product.name}
            image={product.image}
            id={product.id}
            //added
            readyInMinutes={product.readyInMinutes}
            sourceUrl={product.sourceUrl}
            servings={product.servings}
            instructions={product.instructions}
            nutrition={product.nutrition}
            igd_list={product.igd_list}
            //and stuff below
            addToCart={this.props.addToCart}
            productQuantity={this.props.productQuantity}
            updateQuantity={this.props.updateQuantity}
            openModal={this.props.openModal}
          />
        );
      });

    // Empty and Loading States
    let view;
    if (productsData.length <= 0 && !term) {
      view = <LoadingProducts />;
    } else if (productsData.length <= 0 && term) {
      view = <NoResults />;
    } else {
      view = (
        <CSSTransitionGroup
          transitionName="fadeIn"
          transitionEnterTimeout={500}
          transitionLeaveTimeout={300}
          component="div"
          className="products"
        >
          {productsData}
        </CSSTransitionGroup>
      );
    }
    return (<div className="products-wrapper">
    {view}
    </div>);
  }
}

export default Products;
