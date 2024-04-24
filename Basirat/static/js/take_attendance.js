        const studentItems = document.querySelectorAll('.student-item');

        studentItems.forEach(item => {
            const checkbox = item.querySelector('.invisible-checkbox');
            const attendanceStatus = item.querySelector('.attendance-status');

            item.addEventListener('click', () => {
                checkbox.checked = !checkbox.checked;

                if (checkbox.checked) {
                    attendanceStatus.classList.add('bg-success');
                    attendanceStatus.classList.remove('bg-danger');
                    attendanceStatus.textContent = 'Present';
                    // Update server-side attendance status here
                } else {
                    attendanceStatus.classList.add('bg-danger');
                    attendanceStatus.classList.remove('bg-success');
                    attendanceStatus.textContent = 'Absent';
                    // Update server-side attendance status here
                }
            });
        });
        const takeAttendanceBtn = document.querySelector('.take-attendance-btn');

        studentItems.forEach(item => {
            const checkbox = item.querySelector('.invisible-checkbox');
            const attendanceStatus = item.querySelector('.attendance-status');
            attendanceStatus.classList.add('d-none');
            checkbox.classList.add('d-none');
        });
        takeAttendanceBtn.addEventListener('click', () => {
            if (takeAttendanceBtn.classList.contains('btn-success')) {
                takeAttendanceBtn.classList.remove('btn-success');
                takeAttendanceBtn.classList.add('btn-danger');
                takeAttendanceBtn.textContent = 'Undo Attendance';
                studentItems.forEach(item => {
                    const checkbox = item.querySelector('.invisible-checkbox');
                    const attendanceStatus = item.querySelector('.attendance-status');
                    attendanceStatus.classList.remove('d-none');
                });
                // Perform take attendance action here (call an API, etc.)
            } else {
                takeAttendanceBtn.classList.remove('btn-danger');
                takeAttendanceBtn.classList.add('btn-success');
                takeAttendanceBtn.textContent = 'Take Attendance';
                studentItems.forEach(item => {
                    const checkbox = item.querySelector('.invisible-checkbox');
                    const attendanceStatus = item.querySelector('.attendance-status');
                    attendanceStatus.classList.add('d-none');
                    checkbox.classList.add('d-none');
                });
                // Perform undo attendance action here (call an API, etc.)
            }
        });