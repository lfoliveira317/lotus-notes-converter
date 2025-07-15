import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider
} from '@mui/material';
import {
  ViewList as ViewListIcon,
  Description as FormIcon
} from '@mui/icons-material';

const Navigation: React.FC = () => {
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: 240,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: 240,
          boxSizing: 'border-box',
          top: 64, // Height of AppBar
          height: 'calc(100% - 64px)',
        },
      }}
    >
      <List>
        <ListItem disablePadding>
          <ListItemButton
            component={Link}
            to="/"
            selected={location.pathname === '/'}
          >
            <ListItemIcon>
              <ViewListIcon />
            </ListItemIcon>
            <ListItemText primary="Home" />
          </ListItemButton>
        </ListItem>
        
        <Divider />
        
        <ListItem disablePadding>
          <ListItemButton
            component={Link}
            to="/alldocuments"
            selected={location.pathname === '/alldocuments'}
          >
            <ListItemIcon>
              <ViewListIcon />
            </ListItemIcon>
            <ListItemText primary="AllDocuments" />
          </ListItemButton>
        </ListItem>
        
        <Divider />
        
        <ListItem disablePadding>
          <ListItemButton
            component={Link}
            to="/defaultform"
            selected={location.pathname === '/defaultform'}
          >
            <ListItemIcon>
              <FormIcon />
            </ListItemIcon>
            <ListItemText primary="New DefaultForm" />
          </ListItemButton>
        </ListItem>
      </List>
    </Drawer>
  );
};

export default Navigation;