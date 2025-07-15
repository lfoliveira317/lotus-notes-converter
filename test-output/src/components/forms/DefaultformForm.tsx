import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useForm, Controller } from 'react-hook-form';
import {
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Grid
} from '@mui/material';

interface DefaultformData {
  title: string;
  content: string;
  author: string;
  created: string;
}

const DefaultformForm: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { control, handleSubmit, reset, formState: { errors } } = useForm<DefaultformData>();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (id) {
      loadDocument(id);
    }
  }, [id]);

  const loadDocument = async (documentId: string) => {
    try {
      setLoading(true);
      console.log('Loading document:', documentId);
    } catch (error) {
      console.error('Error loading document:', error);
    } finally {
      setLoading(false);
    }
  };

  const onSubmit = async (data: DefaultformData) => {
    try {
      setLoading(true);
      console.log('Saving form data:', data);
      navigate('/all-documents');
    } catch (error) {
      console.error('Error saving form:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        DefaultForm {id ? '(Edit)' : '(New)'}
      </Typography>
      
      <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 2 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Controller
              name="title"
              control={control}
              defaultValue=""
              rules={{ required: 'Title is required' }}
              render={({ field: fieldProps }) => (
                <TextField
                  {...fieldProps}
                  label="Title"
                  fullWidth
                  error={!!errors.title}
                  helperText={errors.title?.message}
                />
              )}
            />
          </Grid>
          <Grid item xs={12}>
            <Controller
              name="content"
              control={control}
              defaultValue=""
              rules={{}}
              render={({ field: fieldProps }) => (
                <TextField
                  {...fieldProps}
                  label="Content"
                  multiline
                  rows={4}
                  fullWidth
                  error={!!errors.content}
                  helperText={errors.content?.message}
                />
              )}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <Controller
              name="author"
              control={control}
              defaultValue=""
              rules={{}}
              render={({ field: fieldProps }) => (
                <TextField
                  {...fieldProps}
                  label="Author"
                  fullWidth
                  error={!!errors.author}
                  helperText={errors.author?.message}
                />
              )}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <Controller
              name="created"
              control={control}
              defaultValue=""
              rules={{}}
              render={({ field: fieldProps }) => (
                <TextField
                  {...fieldProps}
                  label="Created"
                  fullWidth
                  error={!!errors.created}
                  helperText={errors.created?.message}
                />
              )}
            />
          </Grid>
        </Grid>
        
        <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
          <Button
            type="submit"
            variant="contained"
            disabled={loading}
          >
            {loading ? 'Saving...' : 'Save'}
          </Button>
          <Button
            variant="outlined"
            onClick={() => navigate('/all-documents')}
          >
            Cancel
          </Button>
        </Box>
      </Box>
    </Paper>
  );
};

export default DefaultformForm;

