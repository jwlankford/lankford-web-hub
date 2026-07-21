const API_BASE = 'http://localhost:8000/api/v1/book';

export interface SignupInput {
  email: string;
  first_name?: string;
}

export async function checkProfessionalBackendHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/signup`, {
      method: 'OPTIONS'
    });
    return res.ok || res.status === 405; // OPTIONS check
  } catch {
    return false;
  }
}

export async function submitBookMailingList(input: SignupInput): Promise<{ success: boolean; message: string; isLiveBackend: boolean }> {
  try {
    const res = await fetch(`${API_BASE}/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'professional.localhost',
        'X-Tenant': 'professional'
      },
      body: JSON.stringify({
        email: input.email.trim(),
        first_name: input.first_name?.trim() || null,
        tenant: 'professional'
      })
    });

    if (res.ok) {
      return {
        success: true,
        message: `Welcome aboard! ${input.email} has been subscribed to launch updates.`,
        isLiveBackend: true
      };
    } else {
      const data = await res.json().catch(() => ({}));
      return {
        success: false,
        message: data.detail || 'This email address may already be registered.',
        isLiveBackend: true
      };
    }
  } catch (err) {
    console.warn('[Professional Service] Backend offline, simulating subscriber confirmation.', err);
    return {
      success: true,
      message: `[Simulated] Thank you for joining! ${input.email} registered successfully.`,
      isLiveBackend: false
    };
  }
}
