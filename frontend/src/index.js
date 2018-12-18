import React, { Component } from "react";
import ReactDOM from "react-dom";
import axios from "axios";
import Header from "./components/Header";
import Products from "./components/Products";
import Footer from "./components/Footer";
import QuickView from "./components/QuickView";
import "./scss/style.scss";
import Toggle from 'react-toggle'



class App extends Component {
  // constructor to initialize the overall app object
  constructor() {
    super();
    this.state = {
      products: [],
      cart: [],
      totalItems: 0,
      totalAmount: 0,
      totalTime: 0,
      term: "",
      category: "",
      isVegetarianOn: false,
      isGlutenOn: false,
      isDairyOn: false,
      cartBounce: false,
      quantity: 1,
      quickViewProduct: {},
      modalActive: false
    };
    // bind all these functions to the app class instance
    // so that all of these functions are always called on the
    // app object
    // note that the functions are defined as methods below in
    // the class.  But we can put them here because of hoisting?
    this.handleSearch = this.handleSearch.bind(this);
    this.handleMobileSearch = this.handleMobileSearch.bind(this);
    this.handleCategory = this.handleCategory.bind(this);
    this.handleAddToCart = this.handleAddToCart.bind(this);
    this.sumTotalItems = this.sumTotalItems.bind(this);
    this.sumTotalAmount = this.sumTotalAmount.bind(this);
    this.sumTotalTime = this.sumTotalTime.bind(this);
    this.checkProduct = this.checkProduct.bind(this);
    this.updateQuantity = this.updateQuantity.bind(this);
    this.handleRemoveProduct = this.handleRemoveProduct.bind(this);
    this.openModal = this.openModal.bind(this);
    this.closeModal = this.closeModal.bind(this);
    this.getProductsMore = this.getProductsMore.bind(this);
    this.handleClickVegetarian = this.handleClickVegetarian.bind(this);
    this.handleClickGluten = this.handleClickGluten.bind(this);
    this.handleClickDairy = this.handleClickDairy.bind(this);
  }


  handleClickVegetarian() {
  this.setState(state => ({
    isVegetarianOn: !state.isVegetarianOn
  }));
  console.log('veggie swtich');
  console.log(this.state.isVegetarianOn);
  }

  handleClickDairy() {
  this.setState(state => ({
    isDairyOn: !state.isDairyOn
  }));
  }

  handleClickGluten() {
  this.setState(state => ({
    isGlutenOn: !state.isGlutenOn
  }));
  }



  // Fetch Initial Set of Products from external API
  getProductsInit() {
    let url =
      "http://127.0.0.1:5000/recipe";
    // this makes the call to axios
    // to get the data from REST api
    axios.get(url).then(response => {
      // sets the state of the component
      this.setState({
        products: response.data.slice(0,5)
      });
    });
  }


  getProductsMore() {
    let url =
      "http://127.0.0.1:5000/recipe";
    // this makes the call to axios
    // to get the data from REST api
    axios.get(url).then(response => {
      this.setState(function (prevstate, props){
        var newproducts = response.data.slice(
          (prevstate.products.length), (prevstate.products.length+5));
        return {products: prevstate.products.concat(newproducts) }
      })
    })
  }

  componentWillMount() {
    this.getProductsInit();
  }

  // Search by Keyword
  handleSearch(event) {
    this.setState({ term: event.target.value });
  }
  // Mobile Search Reset
  handleMobileSearch() {
    this.setState({ term: "" });
  }
  // Filter by Category
  handleCategory(event) {
    this.setState({ category: event.target.value });
    console.log(this.state.category);
  }
  // Add to Cart
  handleAddToCart(selectedProducts) {
    let cartItem = this.state.cart;
    let productID = selectedProducts.id;
    let productQty = selectedProducts.quantity;
    if (this.checkProduct(productID)) {
      console.log("hi");
      let index = cartItem.findIndex(x => x.id == productID);
      cartItem[index].quantity =
        Number(cartItem[index].quantity) + Number(productQty);
      this.setState({
        cart: cartItem
      });
    } else {
      cartItem.push(selectedProducts);
    }
    this.setState({
      cart: cartItem,
      cartBounce: true
    });
    setTimeout(
      function() {
        this.setState({
          cartBounce: false,
          quantity: 1
        });
        console.log(this.state.quantity);
        console.log(this.state.cart);
      }.bind(this),
      1000
    );
    this.sumTotalItems(this.state.cart);
    this.sumTotalAmount(this.state.cart);
    this.sumTotalTime(this.state.cart);
  }
  handleRemoveProduct(id, e) {
    let cart = this.state.cart;
    let index = cart.findIndex(x => x.id == id);
    cart.splice(index, 1);
    this.setState({
      cart: cart
    });
    this.sumTotalItems(this.state.cart);
    this.sumTotalAmount(this.state.cart);
    e.preventDefault();
  }
  checkProduct(productID) {
    let cart = this.state.cart;
    return cart.some(function(item) {
      return item.id === productID;
    });
  }
  sumTotalItems() {
    let total = 0;
    let cart = this.state.cart;
    total = cart.length;
    this.setState({
      totalItems: total
    });
  }

  // sum the total price
  sumTotalAmount() {
    let total = 0;
    let cart = this.state.cart;
    for (var i = 0; i < cart.length; i++) {
      total += cart[i].price * parseInt(cart[i].quantity);
    }
    this.setState({
      totalAmount: total
    });
  }

  // sum the total cooking time
  sumTotalTime() {
    let total = 0;
    let cart = this.state.cart;
    for (var i = 0; i < cart.length; i++) {
      total += parseInt(cart[i].readyInMinutes) * parseInt(cart[i].quantity);
    }
    this.setState({
      totalTime: total
    });
  }

  //Reset Quantity
  updateQuantity(qty) {
    console.log("quantity added...");
    this.setState({
      quantity: qty
    });
  }
  // Open Modal
  openModal(product) {
    this.setState({
      quickViewProduct: product,
      modalActive: true
    });
  }
  // Close Modal
  closeModal() {
    this.setState({
      modalActive: false
    });
  }

  render() {
    return (
      <div className="container">
        <Header
          cartBounce={this.state.cartBounce}
          total={this.state.totalAmount}
          totalTime={this.state.totalTime}
          totalItems={this.state.totalItems}
          cartItems={this.state.cart}
          removeProduct={this.handleRemoveProduct}
          handleSearch={this.handleSearch}
          handleMobileSearch={this.handleMobileSearch}
          handleCategory={this.handleCategory}
          categoryTerm={this.state.category}
          updateQuantity={this.updateQuantity}
          productQuantity={this.state.moq}
        />
        <div className="wrap-area">



        <div className="toggle-row">
        <label>
          <Toggle
            defaultChecked={this.state.isVegetarianOn}
            onChange={this.handleClickVegetarian} />
          <div>Vegetarian </div>
        </label>
        <label>
          <Toggle
          defaultChecked={this.state.isDairyOn}
          onChange={this.handleClickDairy} />
          <div>Dairy Free </div>
        </label>
        <label>
          <Toggle
          defaultChecked={this.state.isGlutenOn}
          onChange={this.handleClickGluten} />
          <div>Gluten Free</div>
        </label>
        </div>




        <Products
          productsList={this.state.products}
          searchTerm={this.state.term}
          isVegetarianOn={this.state.isVegetarianOn}
          isGlutenOn={this.state.isGlutenOn}
          isDairyOn={this.state.isDairyOn}
          addToCart={this.handleAddToCart}
          productQuantity={this.state.quantity}
          updateQuantity={this.updateQuantity}
          openModal={this.openModal}
        />
        <div className="load-more-div">
        <button onClick={this.getProductsMore} type="button" className="load-more">Load more</button>
       {/* <LoadMoreButton loadMore={this.getProductsMore}/>*/}
        </div>
        </div>

        <Footer />
        <QuickView
          product={this.state.quickViewProduct}
          openModal={this.state.modalActive}
          closeModal={this.closeModal}
        />
      </div>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("root"));
