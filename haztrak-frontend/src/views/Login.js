import React, {useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import {Button, Card, Container, FloatingLabel, Form} from "react-bootstrap";

const Login = props => {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  let navigate = useNavigate()

  const onChangeUsername = e => {
    const username = e.target.value
    setUsername(username)
  }
  const onChangePassword = e => {
    const password = e.target.value
    setPassword(password)
  }

  const login = () => {
    let data = {
      username: username,
      password: password
    }
    props.login(data)
    navigate('/')
  }

  return (
    <Container fluid>
      <div className="row justify-content-center">
        <div className="col-lg-5">
          {/* Login Card */}
          <Card className="shadow-lg border-0 rounded my-5">
            <Card.Header className="py-4 bg-primary text-light text-center">
              <span className="h2">Login</span>
            </Card.Header>
            <Card.Body>
              <Form>
                <Form.Group className="mb-3">
                  <FloatingLabel controlId="usernameInput"
                                 label="Username"
                                 className="mb-3">
                    <Form.Control type="text"
                                  placeholder="Username"
                                  value={username}
                                  onChange={onChangeUsername}
                    />
                  </FloatingLabel>
                  <FloatingLabel controlId="passwordInput"
                                 label="Password"
                                 className="mb-3">
                    <Form.Control type="password"
                                  placeholder="myP@assword"
                                  value={password}
                                  onChange={onChangePassword}
                    />
                  </FloatingLabel>
                  <Form.Check
                    type="switch"
                    id="rememberPasswordInput"
                    label="Remember Password"
                  />
                  <div
                    className="d-flex align-items-center justify-content-end mt-4 mb-0">
                    <Button variant="success" type="button" onClick={login}>
                      Login
                    </Button>
                  </div>
                </Form.Group>
              </Form>
            </Card.Body>
            <Card.Footer>
              <div className="d-flex justify-content-between">
                <Link to="#">Forgot Password?</Link>
                <Link to="/signup">Need an account? Sign up!</Link>
              </div>
            </Card.Footer>
          </Card>
        </div>
      </div>
    </Container>
  )
}

export default Login
