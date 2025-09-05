'use client';

import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, FileText, XCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';

interface FileUploaderProps {
  onFileUpload: (file: File) => void;
  loading: boolean;
}

export function FileUploader({ onFileUpload, loading }: FileUploaderProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setError(null);
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      if (file.type === 'application/pdf') {
        setSelectedFile(file);
        onFileUpload(file);
      } else {
        setError('Only PDF files are allowed.');
        setSelectedFile(null);
      }
    }
  }, [onFileUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    multiple: false,
    disabled: loading,
  });

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setError(null);
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      if (file.type === 'application/pdf') {
        setSelectedFile(file);
        onFileUpload(file);
      } else {
        setError('Only PDF files are allowed.');
        setSelectedFile(null);
      }
    }
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setError(null);
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div
        {...getRootProps()}
        className={cn(
          'flex flex-col items-center justify-center p-6 border-2 border-dashed rounded-lg cursor-pointer transition-colors duration-200',
          isDragActive ? 'border-accent-blue bg-blue-50' : 'border-gray-300 bg-gray-50',
          loading && 'opacity-60 cursor-not-allowed'
        )}
      >
        <Input {...getInputProps()} disabled={loading} />
        {selectedFile ? (
          <div className="flex items-center space-x-2 text-navy-blue">
            <FileText className="h-6 w-6" />
            <span>{selectedFile.name}</span>
            <Button
              variant="ghost"
              size="icon"
              onClick={(e) => {
                e.stopPropagation(); // Prevent dropzone from re-opening
                handleRemoveFile();
              }}
              className="text-red-500 hover:text-red-700"
              disabled={loading}
            >
              <XCircle className="h-4 w-4" />
            </Button>
          </div>
        ) : (
          <>
            <UploadCloud className="h-12 w-12 text-gray-400 mb-3" />
            <p className="text-gray-600 text-center">
              {isDragActive ? 'Drop the PDF here...' : 'Drag & drop your resume (PDF) here, or click to select'}
            </p>
            <p className="text-sm text-gray-500 mt-1">Max file size: 5MB</p>
          </>
        )}
      </div>
      <div className="flex items-center justify-center mt-4">
        <span className="text-gray-500 text-sm">or</span>
      </div>
      <div className="mt-4 flex justify-center">
        <label htmlFor="file-upload" className="cursor-pointer">
          <Button
            asChild
            className="bg-navy-blue hover:bg-gray-700 text-white rounded-md px-6 py-3 transition-colors duration-300 shadow-md"
            disabled={loading}
          >
            <span className="cursor-pointer">Browse Files</span>
          </Button>
          <Input
            id="file-upload"
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="sr-only"
            disabled={loading}
          />
        </label>
      </div>
      {error && <p className="text-red-500 text-sm mt-2 text-center">{error}</p>}
    </div>
  );
}
