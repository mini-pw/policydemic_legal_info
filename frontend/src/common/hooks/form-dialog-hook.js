import { useState, useCallback } from 'react';

export function useFormDialog() {
    const [openDialog, setOpenDialog] = useState(false);

    const handleOpenDialog = useCallback(() => {
        setOpenDialog(true)
    }, [])

    const handleCloseDialog = useCallback(() => {
        setOpenDialog(false)
    }, [])

    return [openDialog, handleOpenDialog, handleCloseDialog];
}