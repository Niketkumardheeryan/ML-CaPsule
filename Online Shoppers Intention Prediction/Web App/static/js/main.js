document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.prediction-form');
    if (!form) {
        return;
    }

    const examples = {
        low: {
            Administrative: 2,
            Administrative_Duration: 45,
            Informational: 1,
            Informational_Duration: 12,
            ProductRelated: 6,
            ProductRelated_Duration: 120,
            BounceRates: 0.72,
            ExitRates: 0.85,
            PageValues: 0.5,
            SpecialDay: 0.0,
            Month: 'Sep',
            VisitorType: 'New Visitor',
            Weekend: 'No',
            OperatingSystems: '1',
            Browser: '1',
            Region: '1',
            TrafficType: '1',
        },
        moderate: {
            Administrative: 5,
            Administrative_Duration: 120,
            Informational: 3,
            Informational_Duration: 90,
            ProductRelated: 18,
            ProductRelated_Duration: 560,
            BounceRates: 0.28,
            ExitRates: 0.22,
            PageValues: 22.4,
            SpecialDay: 0.3,
            Month: 'Nov',
            VisitorType: 'Returning Visitor',
            Weekend: 'No',
            OperatingSystems: '2',
            Browser: '5',
            Region: '3',
            TrafficType: '4',
        },
        high: {
            Administrative: 8,
            Administrative_Duration: 240,
            Informational: 3,
            Informational_Duration: 180,
            ProductRelated: 45,
            ProductRelated_Duration: 2200,
            BounceRates: 0.05,
            ExitRates: 0.07,
            PageValues: 85,
            SpecialDay: 0.8,
            Month: 'Dec',
            VisitorType: 'Returning Visitor',
            Weekend: 'Yes',
            OperatingSystems: '3',
            Browser: '8',
            Region: '5',
            TrafficType: '7',
        },
    };

    const loadButtons = document.querySelectorAll('.load-example');
    loadButtons.forEach((button) => {
        button.addEventListener('click', function () {
            const exampleKey = this.dataset.example;
            const values = examples[exampleKey];
            if (!values) {
                return;
            }
            Object.keys(values).forEach((name) => {
                const field = form.querySelector(`[name="${name}"]`);
                if (field) {
                    field.value = values[name];
                    field.dispatchEvent(new Event('input', { bubbles: true }));
                }
            });
        });
    });

    form.addEventListener('submit', function (event) {
        const fields = form.querySelectorAll('input[type="number"], select');
        let valid = true;

        fields.forEach((field) => {
            if (!field.checkValidity()) {
                valid = false;
                field.parentNode.classList.add('error');
                const message = field.dataset.invalidMessage || 'Please enter a valid value.';
                let error = field.parentNode.querySelector('.field-error');
                if (!error) {
                    error = document.createElement('span');
                    error.className = 'field-error';
                    field.parentNode.appendChild(error);
                }
                error.textContent = message;
            } else {
                field.parentNode.classList.remove('error');
                const error = field.parentNode.querySelector('.field-error');
                if (error) {
                    error.textContent = '';
                }
            }
        });

        if (!valid) {
            event.preventDefault();
        }
    });
});
