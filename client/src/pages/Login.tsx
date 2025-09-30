import { useAuth } from "../context/AuthContent";
import { useNavigate } from "react-router-dom";
import { Box, Button, Container, Typography, Paper } from "@mui/material";
import { useEffect } from "react";
import { Google } from "@mui/icons-material";
import "react-toastify/dist/ReactToastify.css";

const Login = () => {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  useEffect(() => {
    if (user) {
      navigate("/aiagent"); // or your target page
    }
  }, [user, navigate]);

  return (
    <Box>
      <Container maxWidth="xs">
        <Paper elevation={3} sx={{ p: 3, mt: 6 }}>
          <Typography variant="h5" align="left" gutterBottom>
            Sign in to your account
          </Typography>
          <Typography variant="h6" align="center" gutterBottom>
            <Button
              startIcon={<Google />}
              variant="outlined"
              fullWidth
              onClick={login}
              sx={{ mt: 2 }}
            >
              Sign in with Google
            </Button>
          </Typography>
        </Paper>
      </Container>
    </Box>
  );
};

export default Login;
