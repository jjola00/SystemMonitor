import React from "react";

const Navbar = () => {
  return (
    <div style={styles.navbar}>
      <h1 style={styles.title}>System Monitor</h1>
    </div>
  );
};

const styles = {
  navbar: {
    backgroundColor: "#3f51b5",
    padding: "20px",
    color: "#ffffff",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  },
  title: {
    margin: 0,
  },
};

export default Navbar;