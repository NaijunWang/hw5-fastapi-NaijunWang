import React from "react";
import { useState } from "react";
import { SearchOutlined } from '@ant-design/icons';
import { Button, Flex, Input, Typography } from "antd";

export default function Home() {
  const [id, setId] = useState("");
  const [error, setError] = useState("");
  const [product, setProduct] = useState(null);
  const handleClick = async () => {
    try {
      const res = await fetch(`http://localhost:5001/products/${id}`);
      if (!res.ok) {
        const data = await res.json();
        if (Array.isArray(data.detail)) {
          setError(data.detail[0].msg);
        } else {
          setError(data.detail);
        }
        return;
      }

      const data = await res.json();
      setProduct(data);
      setError("");
    } catch (err) {
      setProduct(null);
      setError("Cannot connect to server.");
    }
  };
  return(  
    <>
     <Flex
      vertical
      justify="center"
      align="center"
      style={{height: "100vh"}}
      gap={25}
      >
        <Typography.Title level={1} style={{ margin: 0 }}>
          Search Product By The ID
        </Typography.Title>
        <Flex
        justify="center"
        align="center"
        gap={5}
        >
          <Input placeholder="enter product id" onChange={(e) => setId(e.target.value)} style={{ width: 240 }} />
          <Button type="primary" onClick={handleClick} icon={<SearchOutlined />}>
            Search
          </Button>
        </Flex>

         <Flex>
          {error ? (
            <Typography.Text type="danger">Error: {error}</Typography.Text>
          ) : product ? (
            <ul>
              {Object.entries(product).map(([key, value]) => (
                <li key={key}>
                  <b>{key}:</b> {String(value)}
                </li>
              ))}
            </ul>
          ) : null}
        </Flex>
      </Flex>
    </>
  ); 
}
