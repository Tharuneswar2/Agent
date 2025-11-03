'use client';

import { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { 
  Upload as UploadIcon, 
  File, 
  FileText, 
  CheckCircle, 
  XCircle, 
  Loader2,
  FileSpreadsheet,
  X
} from 'lucide-react';
import { MainLayout } from '@/components/MainLayout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useStore } from '@/store/useStore';
import { cn } from '@/lib/utils';

const mockDocuments = [
  {
    id: '1',
    name: 'Q1_2024_Balance_Sheet.pdf',
    type: 'pdf',
    status: 'completed' as const,
    uploadedAt: new Date('2024-01-15'),
    size: '2.4 MB',
  },
  {
    id: '2',
    name: 'Tesla_Income_Statement_2023.xlsx',
    type: 'xlsx',
    status: 'completed' as const,
    uploadedAt: new Date('2024-01-14'),
    size: '1.8 MB',
  },
  {
    id: '3',
    name: 'Cash_Flow_Analysis.csv',
    type: 'csv',
    status: 'processing' as const,
    uploadedAt: new Date('2024-01-14'),
    size: '856 KB',
  },
];

export default function UploadPage() {
  const [isDragging, setIsDragging] = useState(false);
  const { documents, addDocument } = useStore();
  const [localDocs, setLocalDocs] = useState(mockDocuments);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = Array.from(e.dataTransfer.files);
    files.forEach((file) => {
      const newDoc = {
        id: Date.now().toString() + Math.random(),
        name: file.name,
        type: file.name.split('.').pop() || 'file',
        status: 'uploading' as const,
        uploadedAt: new Date(),
        size: `${(file.size / 1024 / 1024).toFixed(2)} MB`,
      };
      
      setLocalDocs((prev) => [newDoc, ...prev]);
      
      // Simulate upload and processing
      setTimeout(() => {
        setLocalDocs((prev) =>
          prev.map((doc) =>
            doc.id === newDoc.id ? { ...doc, status: 'processing' as const } : doc
          )
        );
      }, 2000);
      
      setTimeout(() => {
        setLocalDocs((prev) =>
          prev.map((doc) =>
            doc.id === newDoc.id ? { ...doc, status: 'completed' as const } : doc
          )
        );
      }, 5000);
    });
  }, []);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    files.forEach((file) => {
      const newDoc = {
        id: Date.now().toString() + Math.random(),
        name: file.name,
        type: file.name.split('.').pop() || 'file',
        status: 'uploading' as const,
        uploadedAt: new Date(),
        size: `${(file.size / 1024 / 1024).toFixed(2)} MB`,
      };
      
      setLocalDocs((prev) => [newDoc, ...prev]);
      
      setTimeout(() => {
        setLocalDocs((prev) =>
          prev.map((doc) =>
            doc.id === newDoc.id ? { ...doc, status: 'processing' as const } : doc
          )
        );
      }, 2000);
      
      setTimeout(() => {
        setLocalDocs((prev) =>
          prev.map((doc) =>
            doc.id === newDoc.id ? { ...doc, status: 'completed' as const } : doc
          )
        );
      }, 5000);
    });
  }, []);

  const getFileIcon = (type: string) => {
    if (type === 'pdf') return FileText;
    if (type === 'xlsx' || type === 'xls' || type === 'csv') return FileSpreadsheet;
    return File;
  };

  const getStatusIcon = (status: string) => {
    if (status === 'completed') return CheckCircle;
    if (status === 'failed') return XCircle;
    return Loader2;
  };

  const getStatusColor = (status: string) => {
    if (status === 'completed') return 'text-green-500';
    if (status === 'failed') return 'text-red-500';
    return 'text-blue-500';
  };

  return (
    <MainLayout>
      <div className="p-8 space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold">Upload Documents</h1>
          <p className="text-muted-foreground mt-1">
            Upload financial statements for analysis
          </p>
        </div>

        {/* Upload Zone */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Card>
            <CardContent className="pt-6">
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={cn(
                  'relative flex flex-col items-center justify-center rounded-lg border-2 border-dashed p-12 transition-colors',
                  isDragging
                    ? 'border-primary bg-primary/5'
                    : 'border-muted-foreground/25 hover:border-primary/50'
                )}
              >
                <UploadIcon className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">
                  Drop files here or click to browse
                </h3>
                <p className="text-sm text-muted-foreground mb-4">
                  Supports PDF, Excel (.xlsx, .xls), and CSV files
                </p>
                <input
                  type="file"
                  multiple
                  accept=".pdf,.xlsx,.xls,.csv"
                  onChange={handleFileInput}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />
                <Button>Select Files</Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Uploaded Documents */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card>
            <CardHeader>
              <CardTitle>Uploaded Documents</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {localDocs.map((doc, index) => {
                  const FileIcon = getFileIcon(doc.type);
                  const StatusIcon = getStatusIcon(doc.status);
                  const statusColor = getStatusColor(doc.status);

                  return (
                    <motion.div
                      key={doc.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="flex items-center gap-4 p-4 rounded-lg border bg-card hover:bg-accent/50 transition-colors"
                    >
                      <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                        <FileIcon className="h-6 w-6 text-primary" />
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        <p className="font-medium truncate">{doc.name}</p>
                        <div className="flex items-center gap-4 mt-1">
                          <span className="text-xs text-muted-foreground">
                            {doc.size}
                          </span>
                          <span className="text-xs text-muted-foreground">
                            {doc.uploadedAt.toLocaleDateString()}
                          </span>
                        </div>
                      </div>

                      <div className="flex items-center gap-2">
                        <StatusIcon
                          className={cn(
                            'h-5 w-5',
                            statusColor,
                            doc.status === 'processing' && 'animate-spin'
                          )}
                        />
                        <span className={cn('text-sm font-medium', statusColor)}>
                          {doc.status === 'uploading' && 'Uploading...'}
                          {doc.status === 'processing' && 'Processing...'}
                          {doc.status === 'completed' && 'Completed'}
                          {doc.status === 'failed' && 'Failed'}
                        </span>
                      </div>

                      <Button variant="ghost" size="icon">
                        <X className="h-4 w-4" />
                      </Button>
                    </motion.div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </MainLayout>
  );
}
