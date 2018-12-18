import React, { Component } from "react";
import Counter from "./Counter";

class Product extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedProduct: {},
      quickViewProdcut: {},
      isAdded: false
    };
  }

  // componentWillMount() {
  //   let image = this.props.image;
  //   let name = this.props.name;
  //   let price = this.props.price;
  //   let id = this.props.id;
  //   let quantity = this.props.productQuantity;
  //   let sourceUrl = this.props.sourceUrl;
  //   let readyInMinutes = this.props.readyInMinutes;
  //   let servings = this.props.servings;
  //   let instructions = this.props.instructions;
  //   let nutrition = this.props.nutrition;
  //   let igd_list = this.props.igd_list;
  //   this.quickView.bind(
  //     this,
  //     image,
  //     name,
  //     price,
  //     id,
  //     readyInMinutes,
  //     sourceUrl,
  //     servings,
  //     instructions,
  //     JSON.parse(JSON.stringify(nutrition)),
  //     igd_list,
  //     //got to put things here
  //     quantity
  // )();}


  addToCart(image, name, price, id, quantity) {
    this.setState(
      {
        selectedProduct: {
          image: image,
          name: name,
          price: price,
          id: id,
          quantity: quantity
        }
      },
      function() {
        this.props.addToCart(this.state.selectedProduct);
      }
    );
    this.setState(
      {
        isAdded: true
      },
      function() {
        setTimeout(() => {
          this.setState({
            isAdded: false,
            selectedProduct: {}
          });
        }, 3500);
      }
    );
  }
  quickView(image, name, price, id, readyInMinutes, sourceUrl, servings, instructions, nutrition, igd_list) {
    this.setState(
      {
        quickViewProdcut: {
          image: image,
          name: name,
          price: price,
          id: id,
          readyInMinutes: readyInMinutes,
          sourceUrl:sourceUrl,
          servings:servings,
          instructions:instructions,
          nutrition:nutrition,
          igd_list:igd_list
        }
      },
      function() {
        this.props.openModal(this.state.quickViewProdcut);
      }
    );
  }
  // the all important render method
  render() {
    let image = this.props.image;
    let name = this.props.name;
    let price = this.props.price;
    let id = this.props.id;
    let quantity = this.props.productQuantity;
    let sourceUrl = this.props.sourceUrl;
    let readyInMinutes = this.props.readyInMinutes;
    let servings = this.props.servings;
    let instructions = this.props.instructions;
    let nutrition = JSON.stringify(this.props.nutrition);
    let igd_list = JSON.stringify(this.props.igd_list);

    // The return statement!
    return (
      <div className="product">
        <div className="product-image">
          <img
            src={image}
            alt={this.props.name}
            onClick={this.quickView.bind(
              this,
              image,
              name,
              price,
              id,
              readyInMinutes,
              sourceUrl,
              servings,
              instructions,
              nutrition,
              igd_list,
              //got to put things here

              quantity
            )}
          />
        </div>
        <h4 className="product-name">{this.props.name}</h4>
        <p className="product-price">{this.props.price}</p>
        <p className=""> Cook time: {this.props.readyInMinutes} minutes</p>

        <br/>
        <Counter
          productQuantity={quantity}
          updateQuantity={this.props.updateQuantity}
          resetQuantity={this.resetQuantity}
        />
        <div className="product-action">
          <button
            className={!this.state.isAdded ? "" : "added"}
            type="button"
            onClick={this.addToCart.bind(
              this,
              image,
              name,
              price,
              id,
              quantity
            )}
          >
            {!this.state.isAdded ? "ADD TO CART" : "✔ ADDED"}
          </button>
        </div>
      </div>
    );
  }
}

export default Product;
