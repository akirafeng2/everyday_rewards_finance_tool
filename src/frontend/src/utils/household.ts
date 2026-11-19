import Cookies from "js-cookie";

export const SAMPLE_MEMBERS = ["Alex", "Adam", "Tyler"];

// household_members cookie holds the backend's household_profile_list (a list of names)
export function getHouseholdMembers(): string[] {
  const raw = Cookies.get("household_members");
  if (!raw) return SAMPLE_MEMBERS;
  try {
    const profiles: Array<string | [number | string, string]> = JSON.parse(raw);
    const names = profiles
      .map((profile) => (Array.isArray(profile) ? profile[1] : profile))
      .filter(Boolean);
    return names.length > 0 ? names : SAMPLE_MEMBERS;
  } catch {
    return SAMPLE_MEMBERS;
  }
}

export function getUserName(): string {
  const name = Cookies.get("user_name") || "Alex";
  return name.charAt(0).toUpperCase() + name.slice(1);
}

export function formatLongDate(date: Date): string {
  return date.toLocaleDateString("en-AU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}
