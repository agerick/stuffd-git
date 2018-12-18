import React, { Component } from "react";

class LoadMoreButton extends Component {
  constructor(props) {
    super(props);
  }

  loadMore(){
    console.log('button load more clicked buddy' + String(Math.random()));
  }

  render() {
    return (
    <button onClick={this.props.loadMore} type="button" className="load-more">Load more</button>
    );
  }
}

export default LoadMoreButton;
